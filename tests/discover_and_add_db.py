import sys
sys.path.append("/home/server/git/RXTNet/xled")
import xled
import mariadb
from contextlib import suppress

# Connect to MariaDB Platform
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