from typing import Optional

import datetime
import task.dao as task_dao

def create(workspace_id: int, name: str, description: str, tags: list = None, due_date: datetime = None, x_location:float = 0, y_location:float = 0):
    """Create a task."""
    if tags is None: tags = []
    return task_dao.create(workspace_id, name, description, tags, due_date, x_location, y_location)

def update(task_id: int, workspace_id: int, name: str = None, description: str = None, tags: list = None, due_date: datetime = None, x_location:float = 0, y_location:float = 0, status: Optional[str] = None) -> bool:
    """Update a task."""
    if tags is None: tags = []
    if task_dao.get_by_id(task_id) is None:
        return False

    return task_dao.update(task_id, workspace_id, name, description, tags, due_date, x_location, y_location, status)

def delete(task_id: int) -> bool:
    """Delete a task."""
    if task_dao.get_by_id(task_id) is None:
        return False

    return task_dao.delete(task_id)

def get(task_id: Optional[str] = None, workspace_id: Optional[str] = None) -> list | None:
    """Get a task by ID, or get all tasks if task_id is None"""
    if task_id is None:
        return task_dao.get_all(workspace_id)
    else:
        return task_dao.get_by_id(task_id)