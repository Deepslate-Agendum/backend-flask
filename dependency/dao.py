from db_python_util.db_classes import Dependency, Field, FieldValue, Task
from db_python_util.db_exceptions import DBException
from db_python_util.db_helper import ConnectionManager

@ConnectionManager.requires_connection
def check_depends_on(dependee_id: str, dependent_id: str) -> str:
    # TODO do some sort of search to determine if there is a transitive dependency between two tasks
    return False

@ConnectionManager.requires_connection
def create_dependency(dependee_id: str, dependent_id: str, manner: str):
    depended_on_task_object = Task.objects.with_id(dependee_id)
    dependent_task_object = Task.objects.with_id(dependent_id)

    duplicates = Dependency.objects(
        depended_on_task=depended_on_task_object,
        dependent_task=dependent_task_object,
    )

    if duplicates.count() > 0:
        raise DBException(f"Dependency already exists between Task(id={dependee_id}) and Task(id={dependent_id})")

    if check_depends_on(dependee_id, dependent_id):
        raise DBException(f"Task(id={dependee_id}) depends on Task(id={dependent_id})")

    manner_field = Field.objects(name = manner)
    manner_field_value = FieldValue(value = 'True', field = manner_field, allowed_value = None)
    manner_field_value.save()

    dependency = Dependency(
        depended_on_task=depended_on_task_object,
        dependent_task=dependent_task_object,
        manner=manner_field_value,
    )
    dependency.save()
    return dependency

@ConnectionManager.requires_connection
def get_all_dependencies():
    pass
