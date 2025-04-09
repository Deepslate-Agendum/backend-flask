import json

from flask import Blueprint, jsonify, request

import user.service as user_service
from be_exceptions.validation_exceptions import ValidationException

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
        return jsonify({"users": users_json}), 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500


@bp.route('/create', methods=['POST'])
def create():
    try:
        username = str(request.json['username'])
        password = str(request.json['password'])
    except Exception as e:
        return jsonify({"Request error" : f"{e}: {str(e)}"}), 400
    try:
        return jsonify({"user.id": user_service.create(username, password)}), 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500

@bp.route('/update', methods=['PATCH'])
def update():
    try:
        user_id = str(request.json['id'])
        username = str(request.json['username'])
        password = str(request.json['password'])
    except Exception as e:
        return jsonify({"Request error" : f"{e}: {str(e)}"}), 400
    try:
        user_service.update(user_id, username, password)
        return "Success", 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500

@bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        user_id = str(request.json['id'])
    except Exception as e:
        return jsonify({"Request error" : f"{e}: {str(e)}"}), 400
    try:
        user_service.delete(user_id)
        return "Success", 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        username = str(request.json['username'])
        password = str(request.json['password'])
    except Exception as e:
        return jsonify({"Request error" : f"{e}: {str(e)}"}), 400
    try:
        user, token = user_service.login(username, password)
        return jsonify({
            "user": json.loads(user.to_json()),  # HACK: same as above, also TODO: if user is null, again depending on AGENDUM-62
            "token": token,
        }), 200
    except ValidationException as e:
        return jsonify({"Validation error": str(e)}), 400
    except Exception as e:
        return jsonify({"Unknown error" : str(e)}), 500

@bp.route('/logout', methods=['POST'])
def logout():
    return "Not Implemented", 501