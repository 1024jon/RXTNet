import mariadb

def dbconnect():
    try:
        conn = mariadb.connect(
            user="root",
            password="1q2w3e4r",
            host="db",
            port=3306,
            database="rxtnet"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)