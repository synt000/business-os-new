TASKS = {}

def save_task(task_id: str, data: dict):
    if task_id not in TASKS:
        TASKS[task_id] = {}
    TASKS[task_id].update(data)


def get_task(task_id: str):
    return TASKS.get(task_id, {"status": "not_found"})
