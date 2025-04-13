from flask import (
    Blueprint,
    request,
    jsonify
)
import be_utilities.response_model as responses
import dependency.service as service
from db_python_util.serialization_helper import get_fields
from db_python_util.db_exceptions import DBException
from be_utilities.validation_exceptions import ValidationException

blueprint = Blueprint(
    name='dependency',
    import_name=__name__,
    url_prefix='/dependency',
)

@blueprint.post('/')
def create_dependency(workspace_id: str):
    try:
        dependee_id = str(request.json['dependee_id'])
        dependent_id = str(request.json['dependent_id'])
        manner = str(request.json['manner'])
    except KeyError as e:
        return responses.request_error_response(e)
    try:
        dependency = service.create(dependee_id, dependent_id, manner)
        return responses.success_response("create_dependency", get_fields(dependency))
    except ValidationException as e:
        return responses.validation_error_response(e)
    except Exception as e:
        return responses.unknown_error_response(e)

@blueprint.get('/')
def get_all_dependencies(workspace_id: str):
    try:
        dependencies = service.get_all(workspace_id)
        return responses.success_response("get_all_dependencies",
            [get_fields(dependency) for dependency in dependencies])
    except ValidationException as e:
        return responses.validation_error_response(e)
    except Exception as e:
        return responses.unknown_error_response(e)

@blueprint.get('/<dependency_id>')
def get_dependency(workspace_id: str, dependency_id: str):
    try:
        dependency = service.get_by_id(dependency_id)
        return responses.success_response("get_fields", get_fields(dependency))
    except ValidationException as e:
        return responses.validation_error_response(e)
    except Exception as e:
        return responses.unknown_error_response(e)

@blueprint.delete('/<dependency_id>')
def delete_dependency(workspace_id: str, dependency_id: str):
    try:
        service.delete(dependency_id)
        return responses.success_response("delete_dependency")
    except ValidationException as e:
        return responses.validation_error_response(e)
    except Exception as e:
        return responses.unknown_error_response(e)

