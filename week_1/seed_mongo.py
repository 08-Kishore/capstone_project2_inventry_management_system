import os
import sys
import json
from datetime import datetime

# Add project root to path so we can import from the config folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.mongo_db import get_mongo_db

def seed_mongo_audit_logs():
    # 1. Connect to MongoDB using config module
    db = get_mongo_db()
    if db is None:
        print("Error: Could not establish a MongoDB connection.")
        return

    collection = db["audit_logs"]

    # 2. Clear existing audit logs collection to prevent duplication on re-runs
    collection.delete_many({})
    print("Cleared existing audit_logs collection.")

    # 3. Load audit logs data from the data folder JSON file
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    json_file_path = os.path.join(data_dir, "sample_audit_logs.json")

    if not os.path.exists(json_file_path):
        print(f"Error: Could not find {json_file_path}. Make sure your data folder is set up correctly.")
        return

    with open(json_file_path, "r", encoding="utf-8") as file:
        audit_data = json.load(file)

    # 4. Insert documents into MongoDB
    if audit_data:
        for doc in audit_data:
            if "timestamp" in doc and isinstance(doc["timestamp"], str):
                doc["timestamp"] = datetime.fromisoformat(doc["timestamp"].replace("Z", "+00:00"))

        result = collection.insert_many(audit_data)
        print(f"Successfully inserted {len(result.inserted_ids)} audit log documents into MongoDB!")

    # 5. Create indexes for quick search by product ID or warehouse[cite: 1]
    print("Creating MongoDB indexes...")
    collection.create_index([("product_id", 1)])
    collection.create_index([("warehouse_id", 1)])
    
    print("MongoDB indexing complete!")

if __name__ == "__main__":
    seed_mongo_audit_logs()