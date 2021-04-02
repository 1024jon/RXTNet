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
    

curselect = conn.cursor(buffered=False)
conID = 43
red = 255
green = 255
blue = 255

curselect.execute("SELECT MacAddress, IP FROM Riverside WHERE ID=conID")
results = curselect.fetchone()

control_interface = xled.ControlInterface(results[1], results[0])
hicontrol = xled.HighControlInterface(results[1])
control_interface.set_mode('movie')
hicontrol.set_static_color(red, green, blue)