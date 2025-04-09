import mysql.connector
from config import Config
def get_db_connection():
    try:
        print("Connecting to DB with:", Config.DB_HOST, Config.DB_USER, Config.DB_NAME)
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            auth_plugin=Config.DB_AUTH_PLUGIN
        )
        return connection
    except mysql.connector.Error as err:
        print(f" Error connecting to MySQL: {err}")
        return None