from flask import (
    Blueprint,
    request,
    jsonify
)

import dependency.service as service
from db_python_util.serialization_helper import get_fields
from db_python_util.db_exceptions import DBException

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

    try:
        dependency = service.create(dependee_id, dependent_id, manner)
    except DBException as e:
        return jsonify({
            "status": "failure",
            "error": e.message
        }), 400

    return jsonify({
        'status': 'success',
        'result': get_fields(dependency),
    }), 200

@blueprint.get('/')
def get_all_dependecies(workspace_id: str):
    try:
        dependencies = service.get_all(workspace_id)
    except DBException as e:
        return jsonify({
            "status": "failure",
            "error": e.message
        }), 400

    return jsonify({
        'status': 'success',
        'result': [get_fields(dependency) for dependency in dependencies],
    }), 200

@blueprint.get('/<dependency_id>')
def get_dependency(workspace_id: str, dependency_id: str):
    try:
        dependency = service.get_by_id(dependency_id)
    except DBException as e:
        return jsonify({
            "status": "failure",
            "error": e.message
        }), 400

    return jsonify({
        'status': 'success',
        'result': get_fields(dependency),
    })

@blueprint.delete('/<dependency_id>')
def delete_dependency(workspace_id: str, dependency_id: str):
    pass
