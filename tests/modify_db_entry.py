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

conID = 43
updateField = 'GroupID'
updateValue = '2'

updatequery = "UPDATE rxtnet.Riverside SET {0}={1} WHERE ID={2}".format(updateField, updateValue, conID)

curupdate = conn.cursor(buffered=False)

curupdate.execute(updatequery)
conn.commit()
conn.close()