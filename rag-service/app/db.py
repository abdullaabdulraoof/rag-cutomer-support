from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"

client = MongoClient(MONGO_URI)
db = client["rag_db"]

chat_collection = db["chat_history"]
faq_collection = db["faq"]