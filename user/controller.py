import json

from flask import Blueprint, jsonify, request

import user.service as user_service
import be_utilities.response_model as responses

from be_utilities.service_exceptions import ServiceException

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'])
@bp.route('/<string:user_id>', methods=['GET'])
def get(user_id: str = None):
    try:
        get_user_result = user_service.get(user_id)
        # HACK: this serializes, deserializes, and then reserializes user. we really need dedicated serialization logic
        # TODO: currently there are no access controls so this leaks password hashes/salts. also we are at the mercy of mongoengine's serialization logic which does weird things
        if isinstance(get_user_result, list):
            users_json = [json.loads(user.to_json()) for user in get_user_result]
        else:
            users_json = json.loads(get_user_result.to_json())
        return responses.success_response("get_users", users_json, "users")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()


@bp.route('/create', methods=['POST'])
def create():
    try:
        username = (request.json['username'])
        password = (request.json['password'])
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        return responses.success_response("create_user", user_service.create(username, password), object_name="user_id")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@bp.route('/update', methods=['PATCH'])
def update():
    try:
        user_id = (request.json['id'])
        username = (request.json['username'])
        password = (request.json['password'])
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        user_service.update(user_id, username, password)
        return responses.success_response("update_user")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        user_id = (request.json['id'])
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        user_service.delete(user_id)
        return responses.success_response("delete_user")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@bp.route('/login', methods=['POST'])
def login():
    try:
        username = (request.json['username'])
        password = (request.json['password'])
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        user, token = user_service.login(username, password)
        return responses.success_response("login_user",
        {"user": json.loads(user.to_json()), "token": token}, object_name="user")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@bp.route('/logout', methods=['POST'])
def logout():
    return "Not Implemented", 501