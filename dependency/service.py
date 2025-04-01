from typing import List

import dependency.dao as dao

def create_dependency(dependee_id: str, dependent_id: str, manner: str):
    manner_id = dao.get_dependency_manner_id(manner)
    dependency = dao.create_dependency(dependee_id, dependent_id, manner_id)
    return dependency

def get_all_dependencies():
    pass

def get_dependencies(dependency_ids: List[str]):
    pass
