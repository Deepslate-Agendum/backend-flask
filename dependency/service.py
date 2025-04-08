from typing import List

import dependency.dao as dao

def create_dependency(dependee_id: str, dependent_id: str, manner: str):
    dependency = dao.create_dependency(dependee_id, dependent_id, manner)
    return dependency

def get_all_dependencies():
    pass

def get_dependencies(dependency_ids: List[str]):
    pass
