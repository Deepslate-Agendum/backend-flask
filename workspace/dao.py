from dao_shared import get_document_by_id
from db_python_util.db_classes import Workspace, TaskType
from db_python_util.db_helper import ConnectionManager

from db_python_util.db_exceptions import (
    EntityNotFoundException,
    UsernameTakenException,
    AlreadyExistsException
)

from mongoengine.errors import (
    ValidationError,
    NotUniqueError,
)


from user.dao import get_by_id as user_get_id

@ConnectionManager.requires_connection
def create(name, owner):
    """
    Create a new empty Workspace
    """

    user_owner = user_get_id(owner)

    default_task_type = TaskType.objects(name = "Default").first()
    try:
        workspace = Workspace(name = name, users = [user_owner], task_types = [default_task_type], tasks = [])
        workspace.save()
    except NotUniqueError:
        raise AlreadyExistsException(f"The workspace {name} already exists.") # should add a more appropriate exception
    return workspace.id.binary.hex()

@ConnectionManager.requires_connection
def get_by_id(workspace_id):
    """
    Get a specific Workspace by its ID
    If the Workspace doesn't exist -> raise EntityNotFoundException
    Else return the Workspace
    """
    workspace = get_document_by_id(Workspace, workspace_id)
    try:
        if workspace == None:
            raise EntityNotFoundException(Workspace, f"No workspace with id '{workspace_id}'")
        return workspace
    except ValidationError as e:
        raise EntityNotFoundException(Workspace, f"No workspace with id '{workspace_id}'")


@ConnectionManager.requires_connection
def get_by_name(name):
    """
    Get a specific Workspace by its name
    If the Workspace doesn't exist -> return None
    Else return the Workspace
    """
    try:
        workspace = Workspace.objects(name = name)
    except ValidationError:
        raise EntityNotFoundException(Workspace, f"")
    if len(workspace) == 0:
        return None

    # TODO in later versions: what to do if multiple workspaces have the same name?
    if len(workspace) > 1:
        return None

    return workspace[0]

@ConnectionManager.requires_connection
def get_all():
    """
    Get all Workspaces
    """

    workspaces = Workspace.objects()

    return workspaces

@ConnectionManager.requires_connection
def update(workspace_id, name, owner):
    """
    Update a specific Workspace by its ID
    """
    workspace = get_by_id(workspace_id)
    if name is not None:
        workspace.update(set__name = name)
    if owner is not None:
        workspace.update(set__users = [owner])

@ConnectionManager.requires_connection
def delete(workspace_id):
    """
    Delete a specific Workspace by its ID
    """
    workspace = get_by_id(workspace_id)
    workspace.delete()
