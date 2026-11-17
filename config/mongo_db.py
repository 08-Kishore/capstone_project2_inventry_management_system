import os
from importlib import import_module

try:
  MongoClient = import_module("pymongo").MongoClient
except ModuleNotFoundError:
  MongoClient = None

try:
  load_dotenv = import_module("dotenv").load_dotenv
  load_dotenv()
except ModuleNotFoundError:
  pass


def get_mongo_db():
  """Returns the specific inventory database instance for audit logs."""
  try:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    client.admin.command("ping")
    db_name = os.getenv("MONGO_DB_NAME", "inventory_db")
    return client[db_name]
  except Exception as err:
    print(f"Error connecting to MongoDB: {err}")
    return None