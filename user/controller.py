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
    try:
        users = user_service.get(user_id)
    except EntityNotFoundException as e:
        return jsonify({"error": e.message}), 404

    # HACK: this serializes, deserializes, and then reserializes user. we really need dedicated serialization logic
    # TODO: currently there are no access controls so this leaks password hashes/salts. also we are at the mercy of mongoengine's serialization logic which does weird things
    if isinstance(users, list):
        users_json = [json.loads(user.to_json()) for user in users]
    else:
        users_json = json.loads(users.to_json())

    return jsonify({"users": users_json}), 200

@bp.route('/create', methods=['POST'])
def create():
    username = request.json['username']
    password = request.json['password']

    try:
        user_id = user_service.create(username, password)
        return jsonify({"user.id": user_id}), 200
    except DBException as e:
        return jsonify({"error": e.message}), 400

@bp.route('/update', methods=['PATCH'])
def update():
    user_id = request.json['id']
    username = request.json['username']
    password = request.json['password']

    try:
        user_service.update(user_id, username, password)
        return "Success", 200
    except DBException as e:
        return jsonify({"error": e.message}), 400

@bp.route('/delete', methods=['DELETE'])
def delete():
    user_id = request.json['id']

    try:
        user_service.delete(user_id)
        return "Success", 200
    except DBException as e:
        return jsonify({"error": e.message}), 400

@bp.route('/login', methods=['POST'])
def login():
    return "Not Implemented", 501

@bp.route('/logout', methods=['POST'])
def logout():
    return "Not Implemented", 501