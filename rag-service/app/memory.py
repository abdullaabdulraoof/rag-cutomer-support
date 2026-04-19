from app.db import chat_collection

def save_chat(session_id, question, answer):
    chat_collection.update_one(
        {"session_id": session_id},
        {
            "$push": {
                "messages": {
                    "$each": [
                        {"sender": "user", "text": question},
                        {"sender": "bot", "text": answer}
                    ]
                }
            }
        },
        upsert=True
    )


def get_chat(session_id):
    chat = chat_collection.find_one({"session_id": session_id})
    return chat["messages"] if chat else []


def clear_chat(session_id):
    chat_collection.delete_one({"session_id": session_id})