from datetime import datetime
import json
import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)
from config.mongo_db import get_mongo_db


def seed_mongo_audit_logs():
  db = get_mongo_db()
  if db is None:
    return

  collection = db["audit_logs"]
  collection.delete_many({})

  data_dir = os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..", "data")
  )
  json_file_path = os.path.join(data_dir, "sample_audit_logs.json")

  with open(json_file_path, "r", encoding="utf-8") as file:
    audit_data = json.load(file)

  if audit_data:
    for doc in audit_data:
      if "timestamp" in doc and isinstance(doc["timestamp"], str):
        doc["timestamp"] = datetime.fromisoformat(
            doc["timestamp"].replace("Z", "+00:00")
        )
    collection.insert_many(audit_data)
    print(
        f"Successfully inserted {len(audit_data)} audit log documents into"
        " MongoDB!"
    )

  # Create Indexes[cite: 1]
  collection.create_index([("product_id", 1)])
  collection.create_index([("warehouse_id", 1)])
  print("MongoDB indexing complete!")


if __name__ == "__main__":
  seed_mongo_audit_logs()