import json

from flask import Blueprint, jsonify, request
import workspace.service as ws_service

import mongoengine.errors as me_errors


bp = Blueprint('workspace', __name__, url_prefix='/workspace')

@bp.route('/create', methods=['POST'])
def create():
    try:
        name = request.json['name']
        owner = request.json['owner']
    except KeyError as e:
        return jsonify({"Request error": f"Missing {str(e)} in request body"}), 400
    errors = ws_service.validate_create(name=name, owner=owner)
    if (len(errors) > 0):
        return jsonify({"Parameter error" : errors}), 400
    workspace_id = ws_service.create(name, owner)
    if workspace_id is not None:
        return jsonify({'workspace.id': workspace_id}), 200 # TODO: no periods in JSON keys
    else:
        return jsonify({"error": "There was a problem creating a workspace"}), 500

@bp.route('/', methods=['GET'])
@bp.route('/<string:workspace_id>', methods=['GET'])
def get(workspace_id: str = None):
    # this seems like a terrible way to validate...
    workspaces = ws_service.get(workspace_id)
    if isinstance(workspaces, me_errors.ValidationError):
        return jsonify({'Parameter error': str(workspaces)}), 400
    # HACK: same deal as in user
    if isinstance(workspaces, list):
        workspaces_json = [json.loads(workspace.to_json()) for workspace in workspaces]
    else:
        workspaces_json = json.loads(workspaces.to_json())

    return jsonify({'workspaces': workspaces_json}), 200

@bp.route('/update', methods=['PATCH'])
def update():
    try:
        workspace_id = request.json['id']
        name = request.json['name']
        owner = request.json['owner']
    except KeyError as e:
        return jsonify({"Request error": f"Missing {str(e)} in request body"}), 400
    errors = ws_service.validate_update(workspace_id, name, owner)
    if len(errors) > 0:
        return jsonify({"Parameter error": errors}), 400
    if ws_service.update(workspace_id, name, owner):
        return "Success", 200
    else:
        return jsonify({"error": "Workspace not found"}), 404

@bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        workspace_id = request.json['id']
    except KeyError as e:
        return jsonify({"Request error": f"Missing {str(e)} in request body"}), 400
    errors = ws_service.validate_delete(workspace_id)
    if len(errors) > 0:
        return jsonify({"Parameter error": errors}), 400
    if ws_service.delete(workspace_id):
        return "Success", 200
    else:
        return jsonify({"error": "Workspace not found"}), 404