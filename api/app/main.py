import sys
#sys.path.append("/usr/src/app")
import dbconnect as dbc
import xled
import mariadb
from contextlib import suppress
import flask
from flask import request, jsonify
import json



app = flask.Flask(__name__) #name flask app
app.config["DEBUG"] = True  #set debug


@app.route('/', methods=['GET'])
def home():
    return '''<h1>RXTNet</h1>
<p>A prototype API for controlling Twinkly lights with ARTNet and web ui control.</p>'''


@app.route('/api/v1/controllers/all', methods=['GET'])
def api_all():
    conn = dbc.dbconnect()  #connect to database, returns db connection object
    curselect = conn.cursor(buffered=False)
    curselect.execute("SELECT * FROM Riverside ORDER BY id ASC;")
    row_headers=[x[0] for x in curselect.description] #this will extract row headers
    controllersdict = curselect.fetchall()
    curselect.close()   
    conn.close() 
    json_data=[]
    for result in controllersdict:
        json_data.append(dict(zip(row_headers,result)))
    
    return json.dumps(json_data), 200

@app.route('/api/v1/controllers/add', methods=['POST'])
def api_add():
    jsondata = request.get_json()
    if 'timeout' in jsondata:
        timeout = int(jsondata['timeout'])
    else:
        return "Need timeout value"
    controllerlist = []
    controllers = xled.discover.xdiscover(None, None, timeout)

    with suppress(xled.exceptions.DiscoverTimeout):
        for controller in controllers:
            controllerlist.append(controller)   
            print(controllerlist)
    try:
        conn = dbc.dbconnect()
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
                conn.close()
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
                conn.close()

    except mariadb.Error as e:
        print(f"Error: {e}")

    return api_all()



@app.route('/api/v1/controllers/id', methods=['GET'])
def api_id(passid = "nopass"):
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if passid == "nopass":
        if 'id' in request.args:
            id = int(request.args['id'])
        else:
            return "Error: No id field provided. Please specify an id."
    else:
        id = int(passid)

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    conn = dbc.dbconnect()
    curselect = conn.cursor(buffered=False)
    dbquery = "SELECT * FROM Riverside WHERE ID={0};".format(id)
    curselect.execute(dbquery)
    row_headers=[x[0] for x in curselect.description] #this will extract row headers
    results = curselect.fetchall()
    curselect.close()  
    conn.close()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))
        
    return json.dumps(json_data)


@app.route('/api/v1/controllers/highlight', methods=['POST'])
def api_highlight():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    jsondata = request.get_json()
        
    if 'id' in jsondata:
        id = int(jsondata['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    conn = dbc.dbconnect()
    curselect = conn.cursor(buffered=False)
    
    dbquery = "SELECT MacAddress, IP FROM Riverside WHERE ID={0}".format(id)

    curselect.execute(dbquery)
    results = curselect.fetchone()
    curselect.close()
    conn.close()

    control_interface = xled.ControlInterface(results[1], results[0])
    hicontrol = xled.HighControlInterface(results[1])
    control_interface.set_mode('movie')
    hicontrol.set_static_color(255,255,255)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return 200

@app.route('/api/v1/controllers/off', methods=['POST'])
def api_controlleroff():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    jsondata = request.get_json()
        
    if 'id' in jsondata:
        id = int(jsondata['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    conn = dbc.dbconnect()
    curselect = conn.cursor(buffered=False)
    
    dbquery = "SELECT MacAddress, IP FROM Riverside WHERE ID={0}".format(id)

    curselect.execute(dbquery)
    results = curselect.fetchone()
    curselect.close()
    conn.close()

    control_interface = xled.ControlInterface(results[1], results[0])
    hicontrol = xled.HighControlInterface(results[1])
    control_interface.set_mode('off')

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return 200


@app.route('/api/v1/controllers/staticcolor', methods=['POST'])
def api_staticcolor():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    jsondata = request.get_json()
    
    if 'id' in jsondata:
        id = int(jsondata['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    
    if 'red' in jsondata:
        red = int(jsondata['red'])
    else:
        return "Error: No red field provided. Please specify an red."
    
    if 'green' in jsondata:
        green = int(jsondata['green'])
    else:
        return "Error: No green field provided. Please specify an green."
    
    if 'blue' in jsondata:
        blue = int(jsondata['blue'])
    else:
        return "Error: No blue field provided. Please specify an blue."

    

    conn = dbc.dbconnect()
    dbquery = "SELECT MacAddress, IP FROM Riverside WHERE ID={0}".format(id)

    curselect.execute(dbquery)
    results = curselect.fetchone()
    curselect.close()
    conn.close()

    control_interface = xled.ControlInterface(results[1], results[0])
    hicontrol = xled.HighControlInterface(results[1])
    control_interface.set_mode('movie')
    hicontrol.set_static_color(red, green, blue)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return 200

@app.route('/api/v1/controllers/groups/all', methods=['GET'])
def api_listgroups():
    #where groupname IS NOT NULL
    conn = dbc.dbconnect()
    dbquery = "SELECT MacAddress, IP, ID, GroupName FROM Riverside WHERE GroupName IS NOT NULL"
    curselect = conn.cursor(buffered=False)
    curselect.execute(dbquery)
    results = curselect.fetchall()
    
    groups = {}
    
    for item in results:
        if item[3] in groups:
            groups[item[3]] += 1
        else:
            groups[item[3]] = 1
    curselect.close()
    conn.close()
    return jsonify(groups)
    
@app.route('/api/v1/controllers/update', methods=['POST'])
def api_update_field():
    #example curl post
    #curl --header "Content-Type: application/json" --request POST --data '{"id":"46","fieldname":"GroupName","value":"test5"}' http://127.0.0.1:8083/api/v1/controllers/update
    jsondata = request.get_json()
    
    if 'id' in jsondata:
        id = int(jsondata['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    
    if 'fieldname' in jsondata:
        fieldname = jsondata['fieldname']
    else:
        return "Error: No field provided. Please specify a field."
    
    if 'value' in jsondata:
        value = jsondata['value']
    else:
        return "Error: No value provided. Please specify a value."
    
    conn = dbc.dbconnect()
    dbquery = "UPDATE Riverside SET {0}='{1}' WHERE ID={2}".format(fieldname, value, id)
    curselect = conn.cursor(buffered=False)
    curselect.execute(dbquery)
    conn.commit()
    
    dbquery = "SELECT * FROM Riverside WHERE ID={0};".format(id)
    curselect.execute(dbquery)
    results = curselect.fetchall()   
    curselect.close()
    conn.close()
    
    return api_id(id)
    #update
    #take in id, field, data for field