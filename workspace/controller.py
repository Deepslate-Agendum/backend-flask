from flask import Blueprint, jsonify, request
import workspace.service as ws_service

bp = Blueprint('workspace', __name__, url_prefix='/workspace')

@bp.route('/create', methods=['POST'])
def create():
    return jsonify({})

@bp.route('/', methods=['GET'])
def get_workspaces():
    return jsonify({"message": "Workspace list"})

@bp.route('/update', methods=['PUT'])
def update():
    return jsonify({})

@bp.route('/delete', methods=['DELETE'])
def delete():
    return jsonify({})