import datetime

def create(name: str, description: str, workspace_id: int, tags: list = None, due_date: datetime = None) -> int:
    return -1

def update(task_id, name, description, tags, workspace_id, due_date) -> bool:
    return False

def delete(task_id) -> bool:
    return False

def get(task_id) -> list | None:
    return None