from typing import List

import dependency.dao as dao
import be_exceptions.validation_exceptions as validation_exceptions


ALLOWED_DEPENDENCY_MANNERS = ["Subtask", "Blocking"]

def create(dependee_id: str, dependent_id: str, manner: str):
    if manner not in ALLOWED_DEPENDENCY_MANNERS:
        raise validation_exceptions.InvalidParameterException(f"The manner {manner} is not a valid dependency type.")
    dependency = dao.create(dependee_id, dependent_id, manner)
    return dependency

def get_all(workspace_id: str):
    return dao.get_all(workspace_id)

def get_by_id(dependency_id: str):
    return dao.get_by_id(dependency_id)

def get_multiple_by_id(dependency_ids: List[str]):
    pass

def delete(dependency_id: str):
    dao.delete(dependency_id)
