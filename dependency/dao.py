from typing import List
from dao_shared import get_document_by_id, get_documents_by_ids
from db_python_util.db_classes import Dependency, ValueType, AllowedValue, Task
from db_python_util.db_exceptions import DBException, EntityNotFoundException
from db_python_util.db_helper import ConnectionManager

import task.dao as task_dao
import workspace.dao as workspace_dao

@ConnectionManager.requires_connection
def get_manner(manner_name: str) -> AllowedValue:
    manner_type = ValueType.objects(name="Manner").first()
    if manner_type is None:
        raise DBException("Manner ValueType not found! Is the database initialized?")

    manner = AllowedValue.objects(value_type=manner_type, value=manner_name).first()
    if manner is None:
        raise EntityNotFoundException(AllowedValue, f"No Manner with name '{manner_name}' could be found!")

    return manner

@ConnectionManager.requires_connection
def check_depends_on(dependee_id: str, dependent_id: str) -> bool:
    # TODO do some sort of search to determine if there is a transitive dependency between two tasks
    return False

@ConnectionManager.requires_connection
def create(dependee_id: str, dependent_id: str, manner_name: str) -> Dependency:
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

    manner = get_manner(manner_name)

    dependency = Dependency(
        depended_on_task=depended_on_task_object,
        dependent_task=dependent_task_object,
        manner=manner,
    )
    dependency.save()

    depended_on_task_object.update(push__dependencies=dependency)
    dependent_task_object.update(push__dependencies=dependency)

    return dependency

@ConnectionManager.requires_connection
def get_all(workspace_id: str) -> List[Dependency]:
    try:
        workspace = workspace_dao.get_by_id(workspace_id)
        task_ids = [task.pk for task in workspace.tasks]
        dependencies = Dependency.objects(
            dependent_task__in=task_ids,
            depended_on_task__in=task_ids,
        )
    except DBException as e:
        raise EntityNotFoundException
    return list(dependencies)

@ConnectionManager.requires_connection
def get_by_id(id: str) -> Dependency:
    try:
        return get_document_by_id(Dependency, id)
    except DBException as e:
        raise EntityNotFoundException

@ConnectionManager.requires_connection
def get_multiple_by_id(dependency_ids: List[str]) -> Dependency:
    return get_documents_by_ids(Dependency, dependency_ids)

def delete(dependency_id: str) -> None:
    dependency = get_by_id(dependency_id)
    dependency.delete()
