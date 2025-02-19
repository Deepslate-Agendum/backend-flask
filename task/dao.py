#skipping dependency for CRUD operations (02/18)
from db_helper import createTagField
from db_classes import Task, TaskType, FieldValue, Field, Workspace


def create(name, description, workspace_id, tags, due_date):
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

    tag_fields = []
    for tag in tags:
        field = Field.objects(name = tag)
        if len(field) == 0:
            tag_field = createTagField(tag)
            tag_fields.append(tag_field)
        else:
            # TODO in later versions: what to do if multiple fields of the same name exist. ie. one is a tag and another is a field
            tag_fields.append(field[0])

    due_date_field = Field.objects(name = "Due Date")
    due_date_field = due_date_field[0]

    # TODO in later versions: split out creating Field Values into a seperate helper function
    # create non-static field values for the new task
    ns_field_values = []
    
    name_field_value = FieldValue(value = name, task_type = None, field = name_field, allowed_value = None)
    name_field_value.save()
    ns_field_values.append(name_field_value)

    description_field_value = FieldValue(value = description, task_type = None, field = description_field, allowed_value = None)
    description_field_value.save()
    ns_field_values.append(description_field_value)

    for field in tag_fields:
        tag_field_value = FieldValue(value = 'True', task_type = None, field = field, allowed_value = None)
        tag_field_value.save()
        ns_field_values.append(tag_field_value)

    due_date_field_value = FieldValue(value = due_date, task_type = None, field = due_date_field, allowed_value = None)
    due_date_field_value.save()
    ns_field_values.append(due_date_field_value)


    # create the task
    task = Task(nonstatic_field_values = ns_field_values, dependencies = [], task_type = default_task_type)
    task.save()


    # update workspace with task
    workspace = Workspace.objects(id = workspace_id)
    workspace.update_one(push__tasks = task)    


def get_by_id(task_id):
    """
    Get the task by id
    If the task does not exist: -> return None
    Else return the task object
    """

    task = Task.objects(id = task_id)
    if len(task) == 0:
        return None
    
    return task[0]

def get_all():
    """
    Get all of the tasks
    Returns a list of task objects
    """

    tasks = Task.objects()

    return tasks

def update(task_id, name, description, tags, workspace_id, due_date):
    """
    Update the task by id
    Currently only supports default task updateality
    """

    task = Task.objects(id = task_id)
    if len(task) == 0:
        return None

    new_tags = tags.copy()

    # go through the current field values and update them
    for field_value in task[0].nonstatic_field_values:
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
                task.update_one(pull__nonstatic_field_values = field_value)
        if field_value_object.field.name == "Due Date":
            if due_date is not None:
                field_value_objects.update_one(set__value = due_date)

    # add the new tags to the task
    for tag in new_tags:
        # check if the tag already exists
        tag_field = Field.objects(name = tag)
        if len(tag_field) == 1: # if one exists then create a new field value and add it to the task
            tag_field_value = FieldValue(value = 'True', task_type = None, field = tag_field[0], allowed_value = None)
            tag_field_value.save()
            task.update_one(push__nonstatic_field_values = tag_field_value) 
        elif len(tag_field) > 1: # if multiple fields with that name exist then grab the one that is a tag
            for field in tag_field:
                if field.value_type.name == "Tag":
                    tag_field_value = FieldValue(value = 'True', task_type = None, field = tag_field[0], allowed_value = None)
                    tag_field_value.save()
                    task.update_one(push__nonstatic_field_values = tag_field_value) 
        else: # if none exist then create a new tag
            tag_field = createTagField(name = tag)
            tag_field_value = FieldValue(value = 'True', task_type = None, field = tag_field, allowed_value = None)
            tag_field_value.save()
            task.update_one(push__nonstatic_field_values = tag_field_value) 


    # get the workspace the task was originally assigned to
    original_workspace = Workspace.objects(tasks__in = [task[0]])
    original_workspace_id = original_workspace[0].id
    if original_workspace_id != workspace_id: # if they aren't the same then update the workspace
        original_workspace.update_one(pull__tasks = task[0])
        
        workspace = Workspace.objects(id = workspace_id)
        workspace.update_one(push__tasks = task[0])



def delete(task_id):
    """
    Delete a task by id
    """

    task = get_by_id(task_id)
    if task is None:
        return

    task.delete()

