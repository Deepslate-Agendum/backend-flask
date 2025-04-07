import json

from flask import Blueprint, jsonify, request

import user.service as user_service
from user_token import service as token_service

from db_python_util.db_exceptions import (
    DBException,
    EntityNotFoundException,
)


bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'])
@bp.route('/<string:user_id>', methods=['GET'])
def get(user_id: str = None):
    get_user_result = user_service.get(user_id)
    if isinstance(get_user_result, EntityNotFoundException):
        return jsonify({"Not found" : str(get_user_result)})
    # HACK: this serializes, deserializes, and then reserializes user. we really need dedicated serialization logic
    # TODO: currently there are no access controls so this leaks password hashes/salts. also we are at the mercy of mongoengine's serialization logic which does weird things
    if isinstance(get_user_result, list):
        users_json = [json.loads(user.to_json()) for user in get_user_result]
    else:
        users_json = json.loads(get_user_result.to_json())

    return jsonify({"users": users_json}), 200

@bp.route('/create', methods=['POST'])
def create():
    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError as e:
        return jsonify({"Request error" : f"{str(e)} is missing from the request body."}), 40
    try:
        user_id = user_service.create(username, password)
        return jsonify({"user.id": user_id}), 200
    except DBException as e:
        return jsonify({"error": e.message}), 400

@bp.route('/update', methods=['PATCH'])
def update():
    try:
        user_id = request.json['id']
        username = request.json['username']
        password = request.json['password']
    except KeyError as e:
        return jsonify({"Request error" : f"{str(e)} is missing from the request body."}), 400

    errors = user_service.validate_update(user_id, username, password)
    if len(errors) > 0:
        return jsonify({"Parameter error(s)" : errors}), 400
    try:
        user_service.update(user_id, username, password)
        return "Success", 200
    except DBException as e:
        return jsonify({"error": e.message}), 400

@bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        user_id = request.json['id']
    except KeyError as e:
        return jsonify({"Request error" : f"{str(e)} is missing from the request body."}), 400
    errors = user_service.validate_delete(user_id)
    if len(errors) > 0:
        return jsonify({"Parameter error(s)" : errors}), 400
    try:
        user_service.delete(user_id)
        return "Success", 200
    except DBException as e:
        return jsonify({"error": e.message}), 400

@bp.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']
    except KeyError as e:
        return jsonify({"Request error" : f"{str(e)} is missing from the request body."}), 400

    user, token = user_service.login(username, password)
    return jsonify({
        "user": json.loads(user.to_json()),  # HACK: same as above, also TODO: if user is null, again depending on AGENDUM-62
        "token": token,
    }), 200

@bp.route('/logout', methods=['POST'])
def logout():
    return "Not Implemented", 501