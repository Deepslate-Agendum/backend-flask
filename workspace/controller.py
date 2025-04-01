import json

from flask import Blueprint, jsonify, request
import workspace.service as ws_service

bp = Blueprint('workspace', __name__, url_prefix='/workspace')

@bp.route('/create', methods=['POST'])
def create():
    name = request.json['name']
    owner = request.json['owner']

    workspace_id = ws_service.create(name, owner)
    if workspace_id is not None:
        return jsonify({'workspace.id': workspace_id}), 200 # TODO: no periods in JSON keys
    else:
        return jsonify({"error": "Workspace name already in use"}), 409

@bp.route('/', methods=['GET'])
@bp.route('/<string:workspace_id>', methods=['GET'])
def get(workspace_id: str = None):
    workspaces = ws_service.get(workspace_id)

    # HACK: same deal as in user
    if isinstance(workspaces, list):
        workspaces_json = [json.loads(workspace.to_json()) for workspace in workspaces]
    else:
        workspaces_json = json.loads(workspaces.to_json())

    return jsonify({'workspaces': workspaces_json}), 200

@bp.route('/update', methods=['PATCH'])
def update():
    workspace_id = request.json['id']
    name = request.json['name']
    owner = request.json['owner']

    if ws_service.update(workspace_id, name, owner):
        return "Success", 200
    else:
        return jsonify({"error": "Workspace not found"}), 404

@bp.route('/delete', methods=['DELETE'])
def delete():
    workspace_id = request.json['id']

    if ws_service.delete(workspace_id):
        return "Success", 200
    else:
        return jsonify({"error": "Workspace not found"}), 404