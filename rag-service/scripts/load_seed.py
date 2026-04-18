import json
from app.db import collection

# Load JSON file
with open("data/seed_data.json", "r") as f:
    data = json.load(f)

# Check if file is empty
if not data:
    print("❌ No data found in seed file")
    exit()

# Optional: Clear old data (for fresh start)
collection.delete_many({})

# Insert data
collection.insert_many(data)

print(f"✅ Inserted {len(data)} records into MongoDB")