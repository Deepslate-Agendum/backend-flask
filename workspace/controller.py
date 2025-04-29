import json

from flask import Blueprint, jsonify, request
import workspace.service as ws_service

workspaces_bp = Blueprint('workspaces', __name__, url_prefix='/workspace')
workspace_bp = Blueprint('workspace', __name__, url_prefix='/<workspace_id>')
workspaces_bp.register_blueprint(workspace_bp)

@workspaces_bp.route('/create', methods=['POST'])
def create():
    name = request.json['name']
    owner = request.json['owner']

    workspace_id = ws_service.create(name, owner)
    if workspace_id is not None:
        return jsonify({'workspace.id': workspace_id}), 200 # TODO: no periods in JSON keys
    else:
        return jsonify({"error": "Workspace name already in use"}), 409

@workspaces_bp.route('/', methods=['GET'])
@workspace_bp.route('/', methods=['GET'])
def get(workspace_id: str = None):
    user_token = request.get('Authorization').split()[1]

    workspaces = ws_service.get(workspace_id, user_token)

    # HACK: same deal as in user
    if isinstance(workspaces, list):
        workspaces_json = [json.loads(workspace.to_json()) for workspace in workspaces]
    else:
        workspaces_json = json.loads(workspaces.to_json())

    return jsonify({'workspaces': workspaces_json}), 200

@workspaces_bp.route('/update', methods=['PATCH'])
def update():
    workspace_id = request.json['id']
    name = request.json['name']
    owner = request.json['owner']

    if ws_service.update(workspace_id, name, owner):
        return "Success", 200
    else:
        return jsonify({"error": "Workspace not found"}), 404

@workspaces_bp.route('/delete', methods=['DELETE'])
def delete():
    workspace_id = request.json['id']

    if ws_service.delete(workspace_id):
        return "Success", 200
    else:
        return jsonify({"error": "Workspace not found"}), 404
