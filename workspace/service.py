import be_utilities.service_exceptions as service_exceptions
import workspace.dao as ws_dao

import user.service as user_service

from db_python_util.db_exceptions import EntityNotFoundException

# TODO: need to fix type annotations here

def create(name: str, owner: str) -> int:
    if user_service.get(owner) == None:
        raise service_exceptions.MissingException(f"The user ID {owner} does not correspond to a known user.")
    if ws_dao.get_by_name(name) is not None:
        raise service_exceptions.AlreadyExistsException(f"The name {name} is an already existing workspace.")
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

def get(workspace_id: int = None) -> list | None:
    """Get a workspace by ID, or all workspaces if no ID is given."""
    if workspace_id is None:
        return ws_dao.get_all()
    else:
        return ws_dao.get_by_id(workspace_id)