from flask import Blueprint, jsonify, request
import workspace.service as ws_service

bp = Blueprint('workspace', __name__, url_prefix='/workspace')

@bp.route('/create', methods=['POST'])
def create():
    name = request.json['name']
    owner = request.json['owner']

    workspace_id = ws_service.create(name, owner)
    if workspace_id >= 0:
        return jsonify({'workspace.id': workspace_id}), 200
    else:
        return jsonify({"error": "Workspace name already in use"}), 409

@bp.route('/', methods=['GET'])
@bp.route('/<int:workspace_id>', methods=['GET'])
def get(workspace_id: int = None):
    workspaces = ws_service.get(workspace_id)

    if workspaces is not None:
        return jsonify({'workspaces': workspaces}), 200
    else:
        return jsonify({"error": "Workspace not found"}), 404

@bp.route('/update', methods=['PUT'])
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