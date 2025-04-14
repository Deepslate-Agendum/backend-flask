#skipping dependency for CRUD operations (02/18)
from typing import Optional


from dao_shared import get_document_by_id
from db_python_util.db_classes import Task, TaskType, Field, FieldValue, Workspace, ValueType
from db_python_util.db_helper import createTagField, ConnectionManager

from mongoengine.errors import (
    ValidationError,
)
from db_python_util.db_exceptions import (
    EntityNotFoundException,
)

import workspace.dao as workspace_dao

@ConnectionManager.requires_connection
def create(workspace_id: str, name: str, description: str, tags: list = None, due_date: str = None, x_location:float = 0, y_location:float = 0):
    """
    Create a new Task
    Currently only supports creating a default Task
    """

    # TODO in later versions: split out getting a task type into a seperate helper function
    # get the default task type for creating a default task
    default_task_type = TaskType.objects(name = "Default")
    default_task_type = default_task_type[0]

    # TODO in later versions: split out getting a Field into a seperate function
    # get the fields for creating field values of the default task type
    name_field = Field.objects(name = "Name")
    name_field = name_field[0]

    description_field = Field.objects(name = "Description")
    description_field = description_field[0]

    # get the tag Value Type
    tag_value_type = ValueType.objects(name="Tag").first()

    tag_fields = []
    for tag in tags:
        field = Field.objects(name = tag, value_type = tag_value_type).first() or createTagField(tag)
        tag_fields.append(field)

    due_date_field = Field.objects(name = "Due Date")
    due_date_field = due_date_field[0]

    x_location_field = Field.objects(name = "X Location").first()
    y_location_field = Field.objects(name = "Y Location").first()

    # TODO in later versions: split out creating Field Values into a seperate helper function
    # create non-static field values for the new task
    ns_field_values = []

    name_field_value = FieldValue(value=name, field=name_field)
    name_field_value.save()
    ns_field_values.append(name_field_value)

    description_field_value = FieldValue(value = description, field = description_field, allowed_value = None)
    description_field_value.save()
    ns_field_values.append(description_field_value)

    for field in tag_fields:
        tag_field_value = FieldValue(value = 'True', field = field, allowed_value = None)
        tag_field_value.save()
        ns_field_values.append(tag_field_value)

    due_date_field_value = FieldValue(value = due_date, field = due_date_field, allowed_value = None)
    due_date_field_value.save()
    ns_field_values.append(due_date_field_value)

    x_location_field_value = FieldValue(value = str(x_location), field = x_location_field, allowed_value = None)
    x_location_field_value.save()
    ns_field_values.append(x_location_field_value)

    y_location_field_value = FieldValue(value = str(y_location), field = y_location_field, allowed_value = None)
    y_location_field_value.save()
    ns_field_values.append(y_location_field_value)


    # create the task
    task = Task(nonstatic_field_values = ns_field_values, dependencies = [], task_type = default_task_type)
    task.save()

    # BUG: doesn't update workspace with the task
    # update workspace with task
    workspace = Workspace.objects(id = workspace_id)
    workspace.update_one(push__tasks = task)

    return task

@ConnectionManager.requires_connection
def get_by_id(id):
    """
    Get the task by id
    If the task does not exist: -> raise EntityNotFoundException
    Else return the task object
    """
    try:
        task = get_document_by_id(Task, id)
    except ValidationError:
        raise EntityNotFoundException(Task, f"No task with {id}")
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
def update(task_id, workspace_id, name, description, tags, due_date, x_location, y_location):
    """
    Update the task by id
    Currently only supports default task updateality
    """
    task = get_by_id(task_id)

    new_tags = tags.copy()

    # go through the current field values and update them
    for field_value in task.nonstatic_field_values:
        field_value_objects = FieldValue.objects(id = field_value.id)
        field_value_object = field_value_objects[0]
        if field_value_object.field.name == "Name":
            if name is not None:
                field_value_objects.update_one(set__value = name)
        if field_value_object.field.name == "Description":
            if description is not None:
                field_value_objects.update_one(set__value = description)
        if field_value_object.field.value_type.name == "Tag":
            if field_value.field.name in tags: # if the tag already exists on the task then take that tag off of the new tags list and do nothing
                new_tags.remove(field_value.field.name)
                continue
            else: # otherwise delete the tag from the task
                task.update(pull__nonstatic_field_values = field_value)
        if field_value_object.field.name == "Due Date":
            if due_date is not None:
                field_value_objects.update_one(set__value = due_date)
        if field_value_object.field.name == "X Location":
            field_value_objects.update_one(set__value = x_location)
        if field_value_object.field.name == "Y Location":
            field_value_objects.update_one(set__value = y_location)

    # get the tag Value Type
    tag_value_type = ValueType.objects(name="Tag").first()

    # add the new tags to the task
    for tag in new_tags:
        tag_field = Field.objects(name=tag, value_type=tag_value_type).first() or createTagField(name=tag)
        tag_field_value = FieldValue(value='True', field=tag_field, allowed_value=None)
        tag_field_value.save()
        task.update(push__nonstatic_field_values=tag_field_value)

    # BUG: current version doesn't update workspaces properly so will need to update this
    # get the workspace the task was originally assigned to
    original_workspace = Workspace.objects(tasks__in = [task]).first()
    if original_workspace != None:
        original_workspace_id = original_workspace.id.binary.hex()
        if original_workspace_id != workspace_id: # if they aren't the same then update the workspace
            original_workspace.update_one(pull__tasks = task[0])

            workspace = Workspace.objects(id = workspace_id)
            workspace.update_one(push__tasks = task[0])

@ConnectionManager.requires_connection
def delete(task_id):
    """
    Delete a task by id
    """
    # TODO: cascading deletes for subtasks
    task = get_by_id(task_id)
    task.delete()