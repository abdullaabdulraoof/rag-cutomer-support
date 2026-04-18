memory_store = {}

def get_memory(session_id):
    return memory_store.get(session_id, [])


def update_memory(session_id, question, answer):
    if session_id not in memory_store:
        memory_store[session_id] = []

    memory_store[session_id].append({
        "question": question,
        "answer": answer
    })

    # keep only last 3 chats (important)
    memory_store[session_id] = memory_store[session_id][-3:]