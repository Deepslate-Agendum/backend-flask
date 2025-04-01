import json

from flask import Blueprint, jsonify, request

import user.service as user_service
from user_token import service as token_service

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'])
@bp.route('/<string:user_id>', methods=['GET'])
def get(user_id: str = None):
    users = user_service.get(user_id)

    if users is None:
        return jsonify({"error": "User not found"}), 404

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

    user_id = user_service.create(username, password)
    if user_id is not None:
        # TODO: periods in JSON keys is cursed
        return jsonify({"user.id": user_id}), 200
    else:
        return jsonify({"error": "Username already in use"}), 409

@bp.route('/update', methods=['PATCH'])
def update():
    user_id = request.json['id']
    username = request.json['username']
    password = request.json['password']

    if user_service.update(user_id, username, password):
        return "Success", 200
    else:
        # TODO: this is not the only reason a update can return False! (the username may already be taken)
        return jsonify({"error": "User not found"}), 404

@bp.route('/delete', methods=['DELETE'])
def delete():
    user_id = request.json['id']

    if user_service.delete(user_id):
        return "Success", 200
    else:
        return jsonify({"error": "User not found"}), 404

@bp.route('/login', methods=['POST'])
def login():
    return "Not Implemented", 501

@bp.route('/logout', methods=['POST'])
def logout():
    return "Not Implemented", 501