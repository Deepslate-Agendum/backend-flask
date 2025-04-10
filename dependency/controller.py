from flask import (
    Blueprint,
    request,
    jsonify
)

import dependency.service as service
from db_python_util.serialization_helper import get_fields
from db_python_util.db_exceptions import DBException
from be_exceptions.validation_exceptions import ValidationException

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
    except Exception as e:
        return jsonify({"Request error" : f"{e}: {str(e)}"}), 400
    try:
        dependency = service.create(dependee_id, dependent_id, manner)
        return jsonify({
            'status': 'success',
            'result': get_fields(dependency),
            }), 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500

@blueprint.get('/')
def get_all_dependencies(workspace_id: str):
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
    try:
        service.delete(dependency_id)
    except DBException as e:
        return jsonify({
            "status": "failure",
            "error": e.message
        }), 400

    return jsonify({'status': 'success'})
