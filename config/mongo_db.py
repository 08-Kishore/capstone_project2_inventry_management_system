import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()


def get_mongo_client():
  """Establishes and returns a MongoDB client instance."""
  try:
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(uri)
    # The ping command is cheap and verifies the connection
    client.admin.command("ping")
    print("Successfully connected to MongoDB.")
    return client
  except Exception as err:
    print(f"Error connecting to MongoDB: {err}")
    return None


def get_mongo_db():
  """Returns the specific inventory database instance for audit logs."""
  client = get_mongo_client()
  if client:
    db_name = os.getenv("MONGO_DB_NAME", "inventory_db")
    return client[db_name]
  return None


if __name__ == "__main__":
  db = get_mongo_db()
  if db is not None:
    print(f"Connected to MongoDB database: {db.name}")