from typing import List

import dependency.dao as dao

def create_dependency(dependee_id: str, dependent_id: str, manner: str):
    dependency = dao.create_dependency(dependee_id, dependent_id, manner)
    return dependency

def update_dependency(dependency_id: str, dependee_id: str, dependent_id: str, manner: str):
    return dao.udpate_dependency(dependency_id=dependency_id, dependee_id=dependee_id, dependent_id=dependent_id, manner=manner)

def get_all_dependencies():
    pass

def get_dependencies(dependency_ids: List[str]):
    pass
