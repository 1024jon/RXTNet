import sys
sys.path.append("/home/server/git/RXTNet/xled")
import xled
import mariadb
from contextlib import suppress
import flask
from flask import request, jsonify

#need to move to db file
try:
    conn = mariadb.connect(
        user="testuser",
        password="1q2w3e4r",
        host="127.0.0.1",
        port=3306,
        database="rxtnet"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>RXTNet</h1>
<p>A prototype API for controlling Twinkly lights with ARTNet and web ui control.</p>'''


@app.route('/api/v1/controllers/all', methods=['GET'])
def api_all():
    curselect = conn.cursor(buffered=False)
    curselect.execute("SELECT * FROM Riverside ORDER BY id ASC;")
    controllersdict = curselect.fetchall()
    curselect.close()    
    return jsonify(controllersdict)

@app.route('/api/v1/controllers/add', methods=['GET'])
def api_add():
    controllerlist = []
    controllers = xled.discover.xdiscover(None, None, 30)

    with suppress(xled.exceptions.DiscoverTimeout):
        for controller in controllers:
            controllerlist.append(controller)   
            print(controllerlist)
    try:
        for con in controllerlist:
            curinsert = conn.cursor(buffered=False)
            curselect = conn.cursor(buffered=False)
            
            curselect.execute("SELECT StartChannel, StartUniverse, NumLEDS, ChannelsPerLED FROM Riverside ORDER BY id DESC LIMIT 1;")
            sel_results = curselect.fetchone()
            curselect.close()
            control_interface = xled.ControlInterface(con.ip_address, con.hw_address)
            device_info = control_interface.get_device_info()
            if not sel_results:
                curinsert.execute("INSERT INTO rxtnet.Riverside(Name, MacAddress, IP, NumLEDS, ChannelsPerLED, StartChannel, StartUniverse) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (con.id, con.hw_address, con.ip_address, device_info["number_of_led"], len(device_info["led_profile"]), '1', '0'))
                conn.commit()
                curinsert.close()
            else:
                startchannel = sel_results[0]
                startuniverse = sel_results[1]
                usedchannels = sel_results[2] * sel_results[3]
                burnedchannels = ((usedchannels//512)-1) + ((512-startchannel+1)%sel_results[3])
                nextaddr = [startuniverse + (usedchannels//512), startchannel + (usedchannels%512) + burnedchannels]
                curinsert.execute("INSERT INTO rxtnet.Riverside(Name, MacAddress, IP, NumLEDS, ChannelsPerLED, StartChannel, StartUniverse) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (con.id, con.hw_address, con.ip_address, device_info["number_of_led"], len(device_info["led_profile"]), nextaddr[1], nextaddr[0]))
                conn.commit()
                curinsert.close()

    except mariadb.Error as e:
        print(f"Error: {e}")

    return api_all()



@app.route('/api/v1/controllers/id', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    curselect = conn.cursor(buffered=False)
    dbquery = "SELECT * FROM Riverside WHERE ID={0};".format(id)
    curselect.execute(dbquery)
    results = curselect.fetchall()
    curselect.close()  

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


@app.route('/api/v1/controllers/highlight', methods=['GET'])
def api_highlight():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    curselect = conn.cursor(buffered=False)
    conID = id
    
    dbquery = "SELECT MacAddress, IP FROM Riverside WHERE ID={0}".format(conID)

    curselect.execute(dbquery)
    results = curselect.fetchone()
    curselect.close()

    control_interface = xled.ControlInterface(results[1], results[0])
    hicontrol = xled.HighControlInterface(results[1])
    control_interface.set_mode('movie')
    hicontrol.set_static_color(255,255,255)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


@app.route('/api/v1/controllers/staticcolor', methods=['GET'])
def api_staticcolor():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    
    if 'red' in request.args:
        red = int(request.args['red'])
    else:
        return "Error: No red field provided. Please specify an red."
    
    if 'green' in request.args:
        green = int(request.args['green'])
    else:
        return "Error: No green field provided. Please specify an green."
    
    if 'blue' in request.args:
        blue = int(request.args['blue'])
    else:
        return "Error: No blue field provided. Please specify an blue."

    curselect = conn.cursor(buffered=False)
    conID = id
    
    dbquery = "SELECT MacAddress, IP FROM Riverside WHERE ID={0}".format(conID)

    curselect.execute(dbquery)
    results = curselect.fetchone()
    curselect.close()

    control_interface = xled.ControlInterface(results[1], results[0])
    hicontrol = xled.HighControlInterface(results[1])
    control_interface.set_mode('movie')
    hicontrol.set_static_color(red, green, blue)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/api/v1/controllers/groups/all', methods=['GET'])
def api_listgroups():
    #where groupname IS NOT NULL
    #create dict
    #if group not in dict, add + 1
    #if in dict + 1
    #return dict
    
#@app.route('/api/v1/controllers/update', methods=['POST?'])
#def api_update_field():
    #update
    #take in id, field, data for field



app.run()