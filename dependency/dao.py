from db_python_util.db_classes import Dependency, ValueType, AllowedValue, Task
from db_python_util.db_exceptions import DBException, EntityNotFoundException
from db_python_util.db_helper import ConnectionManager

import task.dao as task_dao

@ConnectionManager.requires_connection
def get_dependency_manner(manner_name: str):
    manner_type = ValueType.objects(name="Manner").first()
    if manner_type is None:
        raise DBException("Manner ValueType not found! Is the database initialized?")

    manner = AllowedValue.objects(value_type=manner_type, value=manner_name).first()
    if manner is None:
        raise EntityNotFoundException(AllowedValue, f"No Manner with name '{manner_name}' could be found!")

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

@ConnectionManager.requires_connection
def get_all_dependencies():
    pass
