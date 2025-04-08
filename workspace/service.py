import be_exceptions.validation_exceptions as validation_exceptions
import workspace.dao as ws_dao

import user.service as user_service

from db_python_util.db_exceptions import EntityNotFoundException

# TODO: need to fix type annotations here

def create(name: str, owner: str) -> int:
    if user_service.get(name) == None:
        raise validation_exceptions.MissingException(f"The user ID {owner} does not correspond to a known user.")
    if ws_dao.get_by_name(name) is not None:
        raise validation_exceptions.AlreadyExistsException(f"The name {name} is an already existing workspace.")
    """Create a new workspace."""
    return ws_dao.create(name, owner)

def update(workspace_id: str, name: str = None, owner: str = None) -> bool:
    try:
        get(workspace_id)
    except validation_exceptions.ValidationException as e:
        raise e
    user_id_result = user_service.get(owner)
    if isinstance(user_id_result, EntityNotFoundException):
        raise validation_exceptions.MissingException(f"The provided user ID '{owner}' does not correspond to an existing user.")
    """Update a workspace."""
    return ws_dao.update(workspace_id, name, owner)

def delete(workspace_id: str) -> bool:
    try:
        get(workspace_id)
    except validation_exceptions.ValidationException as e:
        raise e
    """Delete a workspace."""
    return ws_dao.delete(workspace_id)

def get(workspace_id: int = None) -> list | None:
    """Get a workspace by ID, or all workspaces if no ID is given."""
    if workspace_id is None:
        return ws_dao.get_all()
    else:
        try:
            result = ws_dao.get_by_id(workspace_id)
            if result == None:
                 raise validation_exceptions.InvalidParameterException(f"The provided workspace ID '{workspace_id}' is not a valid workspace ID.")
            return result
        except EntityNotFoundException as e:
            raise validation_exceptions.MissingException(f"The provided workspace ID '{workspace_id}' does not correspond to an existing workspace.")