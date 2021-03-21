
import xled
import mariadb

import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="testuser",
        password="1q2w3e4r",
        host="127.0.0.1",
        port=3306,
        database="twinkly"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()
try:
    cur.execute("INSERT INTO twinkly.Riverside(Name, MacAddress, IP) VALUES (?, ?, ?)",('Twinkly1', 'ddddddd', '192.168.0.8'))
    conn.commit()
except mariadb.Error as e:
        print(f"Error: {e}")
#controllers = xled.discover.xdiscover(None, None, 10)
#for controller in controllers:
#    try:
#        cur.execute("INSERT INTO twinkly.Riverside(Name, MacAddress, IP) VALUES (?, ?, ?)",('controller.id', 'contr', 'cont'))
#   except mariadb.Error as e:
 #       print(f"Error: {e}")