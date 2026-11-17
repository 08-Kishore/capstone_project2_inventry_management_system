import os
import mysql.connector # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()


def get_mysql_connection():
  """Establishes and returns a connection to the MySQL inventory database."""
  try:
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "inventory_db"),
    )
    if connection.is_connected():
      return connection
  except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    return None