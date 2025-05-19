import os
import json
from config import MEMORY_DIR, MEMORY_LIMIT

def load_memory(user_id):
    path = f"{MEMORY_DIR}/{user_id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {
        "user_id": user_id,
        "username": "",
        "messages": []
    }



def save_memory(user_id, memory_data):
    path = f"{MEMORY_DIR}/{user_id}.json"
    with open(path, "w") as f:
        json.dump(memory_data, f, indent=4)



def add_message(user_id, username, content, timestamp):
    mem = load_memory(user_id)
    if mem["username"] == "":
        mem["username"] = username

    mem["messages"].append({
        "content": content,
        "timestamp": timestamp
    })

    if len(mem["messages"]) > MEMORY_LIMIT:
        mem["messages"].pop(0)
    save_memory(user_id, mem)


# Viết cho vui á chứ éo chạy, nào có ny sẽ sửa