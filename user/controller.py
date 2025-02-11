from flask import Blueprint, jsonify, request

import user.service as user_service
from user_token import service as token_service

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'])
@bp.route('/<int:id>', methods=['GET'])
def get(user_id: int = None):
    users = user_service.get(user_id)

    if users is not None:
        return jsonify({"users": users}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@bp.route('/create', methods=['POST'])
def create():
    username = request.json['username']
    password = request.json['password']

    if user_service.create(username, password):
        return "Success", 200
    else:
        return jsonify({"error": "Username already in use"}), 409

@bp.route('/update', methods=['UPDATE'])
def update():
    user_id = request.json['id']
    username = request.json['username']
    password = request.json['password']

    if user_service.update(user_id, username, password):
        return "Success", 200
    else:
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