from db_python_util.db_classes import Dependency
from db_python_util.db_exceptions import DBException
from db_python_util.db_helper import ConnectionManager

@ConnectionManager.requires_connection
def get_dependency_manner_id(manner_name: str):
    # TODO: actually get manner id (need to add allowed values in db startup script)
    return None

@ConnectionManager.requires_connection
def check_depends_on(dependee_id: str, dependent_id: str) -> str:
    # TODO do some sort of search to determine if there is a transitive dependency between two tasks
    return False

@ConnectionManager.requires_connection
def create_dependency(dependee_id: str, dependent_id: str, manner_id: str):
    duplicates = Dependency.objects(
        depended_on_task=dependee_id,
        dependent_task=dependent_id,
    )

    if duplicates.count() > 0:
        raise DBException(f"Dependency already exists between Task(id={dependee_id}) and Task(id={dependent_id})")

    if check_depends_on(dependee_id, dependent_id):
        raise DBException(f"Task(id={dependee_id}) depends on Task(id={dependent_id})")

    dependency = Dependency(
        depended_on_task=dependee_id,
        dependent_task=dependent_id,
        manner=manner_id,
    )
    dependency.save()
    return dependency

@ConnectionManager.requires_connection
def get_all_dependencies():
    pass
