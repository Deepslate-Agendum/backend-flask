def create(name: str, owner: str) -> int:
    return -1

def update(workspace_id: int, name: str = None, owner: str = None) -> bool:
    return False

def delete(workspace_id: int) -> bool:
    return False

def get(workspace_id: int = None) -> list | None:
    return None