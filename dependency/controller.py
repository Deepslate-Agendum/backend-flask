from flask import (
    Blueprint,
    request,
    jsonify
)

import dependency.service as service
from db_python_util.serialization_helper import get_fields

blueprint = Blueprint(
    name='dependency',
    import_name=__name__,
    url_prefix='/dependency',
)

@blueprint.post('/')
def create_dependency(workspace_id: str):
    dependee_id = request.json['dependee_id']
    dependent_id = request.json['dependent_id']
    manner = request.json['manner']

    dependency = service.create_dependency(dependee_id, dependent_id, manner)

    return jsonify({
        'status': 'success',
        'result': get_fields(dependency),
    }), 200

@blueprint.get('/')
def get_all_depedencies(workspace_id: str):
    return jsonify({
        'status': 'success',
        'result': [],
    }), 200

@blueprint.get('/<dependency_id>')
def get_dependency(workspace_id: str, dependency_id: str):
    pass

@blueprint.delete('/<dependency_id>')
def delete_dependency(workspace_id: str, dependency_id: str):
    pass
