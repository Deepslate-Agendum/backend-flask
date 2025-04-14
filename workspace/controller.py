import json

from flask import Blueprint, jsonify, request
import workspace.service as ws_service
from be_utilities.service_exceptions import ServiceException
import be_utilities.response_model as responses


workspaces_bp = Blueprint('workspaces', __name__, url_prefix='/workspace')
workspace_bp = Blueprint('workspace', __name__, url_prefix='/<workspace_id>')
workspaces_bp.register_blueprint(workspace_bp)

@workspaces_bp.route('/create', methods=['POST'])
def create():
    try:
        name = (request.json['name'])
        owner = (request.json['owner'])
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        return responses.success_response("create_workspace", {"workspace_id" : ws_service.create(name, owner)})
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@workspaces_bp.route('/', methods=['GET'])
@workspace_bp.route('/', methods=['GET'])
def get(workspace_id: str = None):
    try:
        # HACK: same deal as in user
        workspaces = ws_service.get(workspace_id)
        if isinstance(workspaces, list):
            workspaces_json = [json.loads(workspace.to_json()) for workspace in workspaces]
        else:
            workspaces_json = json.loads(workspaces.to_json())
        return responses.success_response("get_workspaces", workspaces_json)
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@workspaces_bp.route('/update', methods=['PATCH'])
def update():
    try:
        workspace_id = (request.json['id'])
        name = (request.json['name'])
        owner = (request.json['owner'])
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        ws_service.update(workspace_id, name, owner)
        return responses.success_response("update_workspace")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@workspaces_bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        workspace_id = (request.json['id'])
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        ws_service.delete(workspace_id)
        return responses.success_response("delete_workspace")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

