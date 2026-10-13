import os
import mysql.connector  # pyright: ignore[reportMissingImports]



def get_mysql_connection():
  """Establishes and returns a connection to the MySQL inventory database."""
  try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "password123"),
        database=os.getenv("MYSQL_DATABASE", "inventory_db"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
    )
    if conn.is_connected():
      print("Successfully connected to MySQL Database.")
      return conn
  except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    return None


if __name__ == "__main__":
  connection = get_mysql_connection()
  if connection and connection.is_connected():
    connection.close()
    print("MySQL connection closed.")