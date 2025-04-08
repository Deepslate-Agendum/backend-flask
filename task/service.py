from typing import Optional

import datetime
import task.dao as task_dao
import workspace.dao as workspace_dao
import workspace.service as ws_service
import be_exceptions.validation_exceptions as validation_exceptions

from db_python_util.db_exceptions import EntityNotFoundException
from mongoengine.errors import ValidationError

def create(workspace_id: str, name: str, description: str, tags: list = None, due_date: datetime = None):

    try:
        ws_service.get(workspace_id)
    except validation_exceptions.ValidationException as e:
        raise e
    if len(name) == 0:
        raise validation_exceptions.InvalidParameterException("The request task does not have a name.")
    """Create a task."""
    if tags is None: tags = []
    return task_dao.create(workspace_id, name, description, tags, due_date)

def update(task_id: int, workspace_id: int, name: str = None, description: str = None, tags: list = None, due_date: datetime = None) -> bool:
    try:
        ws_service.get(workspace_id)
        get(task_id, workspace_id)
    except validation_exceptions.ValidationException as e:
        raise e
    """Update a task."""
    if tags is None: tags = []
    return task_dao.update(task_id, workspace_id, name, description, tags, due_date)

def delete(task_id: int) -> bool:
    """Delete a task."""
    try:
        get(task_id)
    except validation_exceptions.ValidationException as e:
        raise e
    return task_dao.delete(task_id)

def get(task_id: Optional[str] = None, workspace_id: Optional[str] = None) -> list | None:
    """Get a task by ID, or get all tasks if task_id is None"""
    if task_id is None:
        try:
            ws_service.get(workspace_id)
            return task_dao.get_all(workspace_id)
        except ValidationError as e:
            raise e
    else:
        try:
            return task_dao.get_by_id(task_id)
        except EntityNotFoundException as e:
            raise validation_exceptions.MissingException(f"The given task ID '{task_id}' does not correspond to an existing task.")
        except ValidationError as e:
            raise validation_exceptions.InvalidParameterException(f"The given task ID '{task_id} is not a valid task ID.")