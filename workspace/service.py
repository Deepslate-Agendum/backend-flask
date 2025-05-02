import workspace.dao as ws_dao

# TODO: need to fix type annotations here

def create(name: str, owner: str) -> int:
    """Create a new workspace."""

    return ws_dao.create(name, owner)

def update(workspace_id: int, name: str = None, owner: str = None) -> bool:
    """Update a workspace."""
    if ws_dao.get_by_id(workspace_id) is None:
        return False

    return ws_dao.update(workspace_id, name, owner)

def delete(workspace_id: int) -> bool:
    """Delete a workspace."""
    if ws_dao.get_by_id(workspace_id) is None:
        return False

    return ws_dao.delete(workspace_id)

def get(workspace_id: int = None, user_id: str = None) -> list | None:
    """Get a workspace by ID, or all workspaces if no ID is given."""
    if workspace_id is None:
        return ws_dao.get_all(user_id)
    else:
        return ws_dao.get_by_id(workspace_id)
