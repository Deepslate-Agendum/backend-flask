import json

from flask import Blueprint, jsonify, request
import workspace.service as ws_service
from be_exceptions.validation_exceptions import ValidationException
import mongoengine.errors as me_errors


bp = Blueprint('workspace', __name__, url_prefix='/workspace')

@bp.route('/create', methods=['POST'])
def create():
    try:
        name = str(request.json['name'])
        owner = str(request.json['owner'])
    except Exception as e:
        return jsonify({"Request error": f"Missing {str(e)} in request body"}), 400
    try:
        return jsonify(ws_service.create(name, owner)), 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500

@bp.route('/', methods=['GET'])
@bp.route('/<string:workspace_id>', methods=['GET'])
def get(workspace_id: str = None):
    try:
        # HACK: same deal as in user
        workspaces = ws_service.get(workspace_id)
        if isinstance(workspaces, list):
            workspaces_json = [json.loads(workspace.to_json()) for workspace in workspaces]
        else:
            workspaces_json = json.loads(workspaces.to_json())
        return jsonify({'workspaces': workspaces_json}), 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500

@bp.route('/update', methods=['PATCH'])
def update():
    try:
        workspace_id = str(request.json['id'])
        name = str(request.json['name'])
        owner = str(request.json['owner'])
    except Exception as e:
        return jsonify({"Request error": f"Missing {str(e)} in request body"}), 400
    try:
        return jsonify({ws_service.update(workspace_id, name, owner)}), 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500

@bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        workspace_id = str(request.json['id'])
    except Exception as e:
        return jsonify({"Request error": f"Missing {str(e)} in request body"}), 400
    try:
        return jsonify(ws_service.delete(workspace_id)), 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500

