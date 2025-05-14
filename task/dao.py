#skipping dependency for CRUD operations (02/18)
from typing import Optional


from dao_shared import get_document_by_id
from db_python_util.db_classes import Task, TaskType, Field, FieldValue, Workspace, ValueType
from db_python_util.db_helper import create_tag, get_tag, ConnectionManager
from db_python_util.db_exceptions import EntityNotFoundException, DBIntegrityException
from mongoengine.errors import ValidationError

from task.field_manager import FieldManager
import workspace.dao as workspace_dao


@ConnectionManager.requires_connection
def create(workspace_id: str, name: str, description: str, tags: list = None, due_date: str = None, x_location:float = 0, y_location:float = 0):
    """
    Create a new Task
    Currently only supports creating a default Task
    """

    # TODO in later versions: split out getting a task type into a seperate helper function
    # get the default task type for creating a default task
    default_task_type = TaskType.objects(name="Default").first()

    task = Task(task_type=default_task_type)
    task.save()

    field_manager = FieldManager(task)
    field_manager.add_field_value("Name", name)
    field_manager.add_field_value("Description", description)

    for tag_name in tags:
        tag = get_tag(tag_name) or create_tag(tag_name)
        field_manager.add_field_value("Tags", tag)

    field_manager.add_field_value("Due Date", due_date)
    field_manager.add_field_value("X Location", x_location)
    field_manager.add_field_value("Y Location", y_location)

    task.save()

    workspace = Workspace.objects(id = workspace_id)
    workspace.update_one(push__tasks = task)

    return task

@ConnectionManager.requires_connection
def get_by_id(id):
    """
    Get the task by id
    """
    task = get_document_by_id(Task, id)
    return task

@ConnectionManager.requires_connection
def get_all(workspace_id: Optional[str]):
    """
    Get all of the tasks
    Returns a list of task objects
    """

    if workspace_id is None:
        tasks = Task.objects()
    else:
        workspace = workspace_dao.get_by_id(workspace_id)
        task_ids = [task.pk for task in workspace.tasks]
        tasks = Task.objects(id__in=task_ids) # theoretically this makes one request for all the tasks rather than one per task

    return list(tasks)

@ConnectionManager.requires_connection
def update(task_id, workspace_id, name, description, tags, due_date, x_location: float, y_location: float):
    """
    Update the task by id
    Currently only supports default task updateality
    """

    task = get_by_id(task_id)

    field_manager = FieldManager(task)
    if name is not None:
        field_manager.set_field_value("Name", 0, name)

    if description is not None:
        field_manager.set_field_value("Description", 0, description)

    if due_date is not None:
        field_manager.set_field_value("Due Date", 0, due_date)

    if x_location is not None:
        field_manager.set_field_value("X Location", 0, x_location)

    if y_location is not None:
        field_manager.set_field_value("Y Location", 0, y_location)

    expected_tag_values = {
        get_tag(tag_name) or create_tag(tag_name) for tag_name in tags
    }

    actual_tag_values = set()

    for i in range(field_manager.get_field_value_count("Tags") - 1, -1, -1):
        tag = field_manager.get_field_value("Tags", i)

        if tag not in expected_tag_values:
            field_manager.pop_field_value("Tags", i)
        else:
            actual_tag_values.add(tag)

    to_add_tag_values = expected_tag_values - actual_tag_values

    for tag in to_add_tag_values:
        field_manager.add_field_value("Tags", tag)

    # BUG: current version doesn't update workspaces properly so will need to update this
    # get the workspace the task was originally assigned to
    original_workspace = Workspace.objects(tasks__in = [task]).first()
    if original_workspace != None:
        original_workspace_id = original_workspace.id.binary.hex()
        if original_workspace_id != workspace_id: # if they aren't the same then update the workspace
            original_workspace.update_one(pull__tasks = task)

            workspace = Workspace.objects(id = workspace_id)
            workspace.update_one(push__tasks = task)

    return True



@ConnectionManager.requires_connection
def delete(task_id):
    """
    Delete a task by id
    """
    # TODO: cascading deletes for subtasks
    task = get_by_id(task_id)
    if task is None:
        return False

    task.delete()

    return True
