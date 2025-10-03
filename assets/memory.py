conversations = {}

def add_to_memory(key, role, text):
    if key not in conversations:
        conversations[key] = []
    conversations[key].append({"role": role, "text": text})

    # Keep last 10 lines only
    if len(conversations[key]) > 10:
        conversations[key] = conversations[key][-10:]

def get_memory(key):
    return conversations.get(key, [])

def clear_memory(key):
    if key in conversations:
        del conversations[key]