import workspace.dao as ws_dao

import user.service as user_service

# TODO: need to fix type annotations here

def create(name: str, owner: str) -> int:
    _ = user_service.get(owner)
    _ = ws_dao.get_by_name(name)
    """Create a new workspace."""
    return ws_dao.create(name, owner)

def update(workspace_id: str, name: str = None, owner: str = None) -> bool:
    get(workspace_id)
    _ = user_service.get(owner)
    """Update a workspace."""
    return ws_dao.update(workspace_id, name, owner)

def delete(workspace_id: str):
    get(workspace_id)
    """Delete a workspace."""
    ws_dao.delete(workspace_id)

def get(workspace_id: str = None) -> list:
    """Get a workspace by ID, or all workspaces if no ID is given."""
    if workspace_id is None:
        return ws_dao.get_all()
    else:
        return ws_dao.get_by_id(workspace_id)