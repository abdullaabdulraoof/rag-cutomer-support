import json
import os
from app.db import faq_collection

def seed_data():
    file_path = "data/seed_data.json"

    # ✅ Check file exists
    if not os.path.exists(file_path):
        print("❌ seed_data.json not found")
        return

    # ✅ Load JSON
    with open(file_path, "r") as f:
        data = json.load(f)

    if not data:
        print("❌ No data found in seed file")
        return

    # ✅ Clear old data
    faq_collection.delete_many({})

    # ✅ Insert new data
    faq_collection.insert_many(data)

    print(f"✅ Inserted {len(data)} records into MongoDB")


if __name__ == "__main__":
    seed_data()