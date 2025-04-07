from typing import Optional

import datetime
import task.dao as task_dao
import workspace.dao as workspace_dao

import db_python_util.db_exceptions as db_exceptions
import mongoengine.errors as mongo_errors

def validate_create(workspace_id: int, name: str, description: str, tags: list = None, due_date: datetime = None):
    errors = []
    try:
        if workspace_dao.get_by_id(workspace_id=workspace_id) == None:
            errors.append(f"{str(workspace_id)} is not a valid workspace ID.")
    except mongo_errors.ValidationError as e:
        errors.append(str(e))
    if name == None:
        errors.append("Missing name")
    if description == None:
        errors.append("Missing description")
    return errors

def create(workspace_id: str, name: str, description: str, tags: list = None, due_date: datetime = None):
    """Create a task."""
    if tags is None: tags = []
    return task_dao.create(workspace_id, name, description, tags, due_date)

def update(task_id: int, workspace_id: int, name: str = None, description: str = None, tags: list = None, due_date: datetime = None) -> bool:
    """Update a task."""
    if tags is None: tags = []
    if task_dao.get_by_id(task_id) is None:
        return False

    return task_dao.update(task_id, workspace_id, name, description, tags, due_date)

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