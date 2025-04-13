from flask import (
    Blueprint,
    request,
    jsonify
)
import be_utilities.response_model as responses
from dao_shared import serialize_id
import dependency.service as service
from db_python_util.db_exceptions import DBException
from be_utilities.validation_exceptions import ValidationException

blueprint = Blueprint(
    name='dependency',
    import_name=__name__,
    url_prefix='/dependency',
)

def responsify_dependency(dependency):
    return {
        'id': serialize_id(dependency.id),
        'dependee': serialize_id(dependency.depended_on_task.id),
        'dependent': serialize_id(dependency.dependent_task.id),
        'manner': dependency.manner.value
    }

@blueprint.post('/')
def create_dependency(workspace_id: str):
    try:
        dependee_id = str(request.json['dependee_id'])
        dependent_id = str(request.json['dependent_id'])
        manner = str(request.json['manner'])
    except KeyError as e:
        return responses.request_error_response(str(e), type=type(e).__name__)
    try:
        dependency = service.create(dependee_id, dependent_id, manner)
        return responses.success_response("create_dependency",responsify_dependency(dependency))
    except ValidationException as e:
        return responses.validation_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response(message=str(e), type=type(e).__name__)


@blueprint.get('/')
def get_dependencies(workspace_id: str):
    try:
        ids = request.args.get('ids')
        if ids is None:
            dependencies = service.get_all(workspace_id)
        else:
            ids = ids.split(',')
            dependencies = service.get_multiple_by_id(ids)
        return responses.success_response("get_all_dependencies",
            dependencies)
    except ValidationException as e:
        return responses.validation_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response(message=str(e), type=type(e).__name__)

@blueprint.delete('/<dependency_id>')
def delete_dependency(workspace_id: str, dependency_id: str):
    try:
        service.delete(dependency_id)
        return responses.success_response("delete_dependency")
    except ValidationException as e:
        return responses.validation_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response(message=str(e), type=type(e).__name__)

