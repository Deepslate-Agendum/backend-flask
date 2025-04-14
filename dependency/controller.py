from flask import (
    Blueprint,
    request,
    jsonify
)
import be_utilities.response_model as responses
from dao_shared import serialize_id
import dependency.service as service


from be_utilities.util_funcs import KNOWN_EXCEPTIONS

from be_utilities.util_funcs import get_param_from_body as body
from be_utilities.util_funcs import get_param_from_url as url

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
        dependee_id = body(request, "dependee_id")
        dependent_id = body(request, "dependent_id")
        manner = body(request, "manner")
        dependency = service.create(dependee_id, dependent_id, manner)
        return responses.success_response("create_dependency",responsify_dependency(dependency))
    except KNOWN_EXCEPTIONS as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()


@blueprint.get('/')
def get_dependencies(workspace_id: str):
    try:
        ids = url(request, 'ids')
        if ids is None:
            dependencies = service.get_all(workspace_id)
        else:
            ids = ids.split(',')
            dependencies = service.get_multiple_by_id(ids)

        return responses.success_response("get_dependencies",
            [responsify_dependency(dependency) for dependency in dependencies], object_name="dependency")
    except KNOWN_EXCEPTIONS as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@blueprint.delete('/<dependency_id>')
def delete_dependency(workspace_id: str, dependency_id: str):
    try:
        service.delete(dependency_id)
        return responses.success_response("delete_dependency")
    except KNOWN_EXCEPTIONS as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

