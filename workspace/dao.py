#TODO: Update imports with submodules

def create(name, owner):
    """
    Create a new empty Workspace
    """

    workspace = Workspace(name = name, users = [owner], task_types = [], tasks = [])
    workspace.save()

    return workspace.pk()

def get_by_id(workspace_id):
    """
    Get a specific Workspace by its ID
    If the Workspace doesn't exist -> return None
    Else return the Workspace
    """

    workspace = Workspace.objects(id = workspace_id)
    if len(workspace) == 0:
        return None

    return workspace[0]

def get_by_name(name):
    """
    Get a specific Workspace by its name
    If the Workspace doesn't exist -> return None
    Else return the Workspace
    """

    workspace = Workspace.objects(name = name)
    if len(workspace) == 0:
        return None

    # TODO in later versions: what to do if multiple workspaces have the same name?
    if len(workspace) > 1:
        return None

    return workspace[0]

def get_all():
    """
    Get all Workspaces
    """

    workspaces = Workspace.objects()

    return workspaces

def update(workspace_id, name, owner):
    """
    Update a specific Workspace by its ID
    """

    workspace = Workspace.objects(id = workspace_id)
    if len(workspace) == 0:
        return None
    
    if name is not None:
        workspace.update_one(set__name = name)
    if owner is not None:
        workspace.update_one(set__users = [owner])

    return True

def delete(workspace_id):
    """
    Delete a specific Workspace by its ID
    """

    workspace = get_by_id(workspace_id)
    if (workspace is None):
        return False

    workspace.delete()

    return True
