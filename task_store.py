import json
import redis

r = redis.Redis(host="127.0.0.1", port=6379, db=1)

def save_task(task_id: str, data: dict):
    r.set(task_id, json.dumps(data))

def get_task(task_id: str):
    data = r.get(task_id)
    if not data:
        return {"status": "not_found"}

    return json.loads(data)
