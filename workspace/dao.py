from dao_shared import get_document_by_id
from db_python_util.db_classes import Workspace, TaskType
from db_python_util.db_helper import ConnectionManager
import user.dao as user_dao


@ConnectionManager.requires_connection
def create(name, owner):
    """
    Create a new empty Workspace
    """
    user_owner = user_dao.get_by_id(owner)

    # check if workspace has the same name
    same_name_workspaces = get_by_name(name)
    if (same_name_workspaces is not None):
        for workspace in same_name_workspaces:
            if user_owner in workspace.users:
                return None

    default_task_type = TaskType.objects(name = "Default").first()

    workspace = Workspace(name = name, users = [user_owner], task_types = [default_task_type], tasks = [])
    workspace.save()

    return workspace.id.binary.hex()

@ConnectionManager.requires_connection
def get_by_id(workspace_id):
    """
    Get a specific Workspace by its ID
    """
    return get_document_by_id(Workspace, workspace_id)

@ConnectionManager.requires_connection
def get_by_name(name):
    """
    Get a specific Workspace by its name
    If the Workspace doesn't exist -> return None
    Else return the Workspace
    """

    workspaces = Workspace.objects(name = name)
    if len(workspaces) == 0:
        return None

    return workspaces

@ConnectionManager.requires_connection
def get_all(user_id):
    """
    Get all Workspaces
    """

    workspaces = Workspace.objects(users = user_id)

    return workspaces

@ConnectionManager.requires_connection
def update(workspace_id, username, userid):
    """
    Update a specific Workspace by its ID
    """

    workspace = Workspace.objects(id = workspace_id).first()
    
    if username is not None:
        user = user_dao.get_by_username(username)
        workspace.update(push__users = user)

    if userid is not None:
        user = user_dao.get_by_id(userid)
        workspace.update(pull__users = user)


    return True

@ConnectionManager.requires_connection
def delete(workspace_id):
    """
    Delete a specific Workspace by its ID
    """

    # TODO: Delete tasks in the workspace
    workspace = get_by_id(workspace_id)
    if (workspace is None):
        return False

    workspace.delete()

    return True
