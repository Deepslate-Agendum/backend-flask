from typing import List

from db_python_util.db_classes import Dependency
import dependency.dao as dao


def create(dependee_id: str, dependent_id: str, manner: str):
    dependency = dao.create(dependee_id, dependent_id, manner)
    return dependency

def get_all(workspace_id: str):
    return dao.get_all(workspace_id)

def get_by_id(dependency_id: str):
    return dao.get_by_id(dependency_id)

def get_multiple_by_id(dependency_ids: List[str]) -> List[Dependency]:
    return dao.get_multiple_by_id(dependency_ids)

def delete(dependency_id: str):
    dao.delete(dependency_id)
