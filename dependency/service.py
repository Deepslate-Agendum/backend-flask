from typing import List

import dependency.dao as dao

def create(dependee_id: str, dependent_id: str, manner: str):
    dependency = dao.create(dependee_id, dependent_id, manner)
    return dependency

def get_all(workspace_id: str):
    pass

def get_multiple_by_id(dependency_ids: List[str]):
    pass
