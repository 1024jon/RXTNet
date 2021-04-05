import mariadb

def dbconnect():
    try:
        conn = mariadb.connect(
            user="testuser",
            password="1q2w3e4r",
            host="127.0.0.1",
            port=3306,
            database="rxtnet"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)