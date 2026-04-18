from pymongo import MongoClient

# MongoDB connection URL
MONGO_URI = "mongodb://localhost:27017"

# Create client
client = MongoClient(MONGO_URI)

# Select database
db = client["rag_db"]

# Select collection
collection = db["faq"]