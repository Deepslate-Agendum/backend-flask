from flask import (
    Blueprint,
    request,
    jsonify
)

from dao_shared import serialize_id
import dependency.service as service
from db_python_util.db_exceptions import DBException

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
        'result': responsify_dependency(dependency),
    }), 200

@blueprint.get('/')
def get_dependencies(workspace_id: str):
    try:
        ids = request.args.get('ids')
        if ids is None:
            dependencies = service.get_all(workspace_id)
        else:
            ids = ids.split(',')
            dependencies = service.get_multiple_by_id(ids)
    except DBException as e:
        return jsonify({
            "status": "failure",
            "error": e.message
        }), 400

    return jsonify({
        'status': 'success',
        'result': [responsify_dependency(dependency) for dependency in dependencies],
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
        'result': responsify_dependency(dependency),
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
