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

cur = conn.cursor()
controllerlist = []
#try:
    #cur.execute("INSERT INTO rxtnet.Riverside(Name, MacAddress, IP, NumLEDS, ChannelsPerLED, StartChannel) VALUES (?, ?, ?, ?, ?, ?)",('Twinkly1', 'ddddddd', '192.168.0.8', '250', '3', '(0,0)'))
    #conn.commit()
#except mariadb.Error as e:
        #print(f"Error: {e}")
controllers = xled.discover.xdiscover(None, None, 30)

with suppress(xled.exceptions.DiscoverTimeout):
    for controller in controllers:
        controllerlist.append(controller)   
        print(controllerlist)
try:
    for con in controllerlist:
        control_interface = xled.ControlInterface(con.ip_address, con.hw_address)
        device_info = control_interface.get_device_info()
        cur.execute("INSERT INTO rxtnet.Riverside(Name, MacAddress, IP, NumLEDS, ChannelsPerLED, StartChannel) VALUES (?, ?, ?, ?, ?, ?)",
                (con.id, con.hw_address, con.ip_address, device_info["number_of_led"], len(device_info["led_profile"]), '(0,0)'))
        conn.commit()
except mariadb.Error as e:
    print(f"Error: {e}")