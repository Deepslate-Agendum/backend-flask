from typing import Optional

import datetime
import task.dao as task_dao
import workspace.service as ws_service
import be_utilities.service_exceptions as service_exceptions

def create(workspace_id: str, name: str, description: str, tags: list = None, due_date: datetime = None, x_location = 0.0, y_location = 0.0):
    ws_service.get(workspace_id)
    if len(name) == 0:
        raise service_exceptions.InvalidParameterException("The request task does not have a name.")
    """Create a task."""
    if tags is None: tags = []
    return task_dao.create(workspace_id, name, description, tags, due_date, x_location, y_location)

def update(task_id: str, workspace_id: str, name: str = None, description: str = None, tags: list = None, due_date: datetime = None, x_location:float = 0, y_location:float = 0):
    ws_service.get(workspace_id)
    get(task_id, workspace_id)
    """Update a task."""
    if tags is None: tags = []
    task_dao.update(task_id, workspace_id, name, description, tags, due_date, x_location, y_location)

def delete(task_id: str):
    """Delete a task."""
    get(task_id)
    task_dao.delete(task_id)

def get(task_id: Optional[str] = None, workspace_id: Optional[str] = None) -> list:
    """Get a task by ID, or get all tasks if task_id is None"""
    if task_id is None:
        ws_service.get(workspace_id)
        return task_dao.get_all(workspace_id)
    else:
        return task_dao.get_by_id(task_id)
