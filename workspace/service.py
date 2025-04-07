import workspace.dao as ws_dao
import user.dao as user_dao

import user.service as user_service

import mongoengine.errors as me_errors
from db_python_util.db_exceptions import EntityNotFoundException

# TODO: need to fix type annotations here

def validate_create(name: str, owner: str):
    errors = []
    if name == None:
        errors.append("No name was provided for the workspace.")
    if user_dao.get_by_id(owner) == None:
        errors.append(f"The user ID {owner} does not correspond to a known user.")
    if ws_dao.get_by_name(name) is not None:
        errors.append(f"The name {name} is an already existing workspace.")
    return errors

def create(name: str, owner: str) -> int:
    """Create a new workspace."""
    return ws_dao.create(name, owner)

def validate_update(workspace_id: str, name: str = None, owner: str = None):
    errors = []
    ws_id_result = get(workspace_id)
    if  ws_id_result is None:
        errors.append(f"The provided workspace ID '{workspace_id}' does not correspond to an existing workspace.")
    elif isinstance(ws_id_result, me_errors.ValidationError):
        errors.append(f"The provided workspace ID '{workspace_id}' is not a valid workspace ID.")
    if owner == None:
        errors.append("There is no provided owner ID.")
    user_id_result = user_service.get(owner)
    if isinstance(user_id_result, EntityNotFoundException):
        errors.append(f"The provided user ID '{owner}' is not a valid user ID.")
    return errors

def update(workspace_id: str, name: str = None, owner: str = None) -> bool:
    """Update a workspace."""
    return ws_dao.update(workspace_id, name, owner)


def validate_delete(workspace_id: str):
    errors = []
    ws_id_result = get(workspace_id)
    if  ws_id_result is None:
        errors.append(f"The provided workspace ID '{workspace_id}' does not correspond to an existing workspace.")
    elif isinstance(ws_id_result, me_errors.ValidationError):
        errors.append(f"The provided workspace ID '{workspace_id}' is not a valid workspace ID.")
    return errors

def delete(workspace_id: str) -> bool:
    """Delete a workspace."""
    return ws_dao.delete(workspace_id)

def get(workspace_id: int = None) -> list | None:
    """Get a workspace by ID, or all workspaces if no ID is given."""
    if workspace_id is None:
        return ws_dao.get_all()
    else:
        try:
            return ws_dao.get_by_id(workspace_id)
        except me_errors.ValidationError as e:
            return e
        except EntityNotFoundException as e:
            return e
