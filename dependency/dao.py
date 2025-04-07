from db_python_util.db_classes import Dependency, ValueType, AllowedValue, Task
from db_python_util.db_exceptions import DBException, EntityNotFoundException
from db_python_util.db_helper import ConnectionManager

import task.dao as task_dao

@ConnectionManager.requires_connection
def get_dependency_manner(manner_name: str):
    manner_type = ValueType.objects(name="manner").first()
    if manner_type is None:
        raise DBException("Manner ValueType not found! Is the database initialized?")

    manner = AllowedValue.objects(value_type=manner_type, value=manner_name).first()
    if manner is None:
        raise EntityNotFoundException(f"No Manner with name {manner_name} could be found!")

    return manner

@ConnectionManager.requires_connection
def check_depends_on(dependee_id: str, dependent_id: str) -> str:
    # TODO do some sort of search to determine if there is a transitive dependency between two tasks
    return False

@ConnectionManager.requires_connection
def create_dependency(dependee_id: str, dependent_id: str, manner_name: str):
    depended_on_task_object = task_dao.get_by_id(dependee_id)
    dependent_task_object = task_dao.get_by_id(dependent_id)

    duplicates = Dependency.objects(
        depended_on_task=depended_on_task_object,
        dependent_task=dependent_task_object,
    )

    if duplicates.count() > 0:
        raise DBException(f"Dependency already exists between Task(id={dependee_id}) and Task(id={dependent_id})")

    if check_depends_on(dependee_id, dependent_id):
        raise DBException(f"Task(id={dependee_id}) depends on Task(id={dependent_id})")

    manner = get_dependency_manner(manner_name)

    dependency = Dependency(
        depended_on_task=depended_on_task_object,
        dependent_task=dependent_task_object,
        manner=manner,
    )
    dependency.save()
    return dependency

# def udpate_dependency(dependency_id: str, dependee_id: str, dependent_id: str, manner: str):
#     dependency = Dependency.objects.with_id(dependency_id)
#     if dependency == None:
#         raise EntityNotFoundException(f"Task(id={dependency_id}) not found")

#     depended_on_task_object = Task.objects.with_id(dependee_id)
#     if depended_on_task_object == None:
#         raise EntityNotFoundException(f"Depended on task(id={dependee_id}) not found")

#     dependent_task_object = Task.objects.with_id(dependent_id)
#     if dependent_task_object == None:
#         raise EntityNotFoundException(f"Dependent task(id={dependent_id}) not found")

#     manner_field_value = dependency.manner
#     if manner != manner_field_value.value:
#         manner_field_value.delete()
#         manner_field = Field.objects(name = manner)
#         manner_field_value = FieldValue(value = 'True', field = manner_field, allowed_value = None)
#         manner_field_value.save()

#     dependency.update(
#         depended_on_task=depended_on_task_object,
#         dependent_task=dependent_task_object,
#         manner=manner_field_value,
#     )

#     return

@ConnectionManager.requires_connection
def get_all_dependencies():
    pass
