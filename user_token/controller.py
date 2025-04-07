from flask import Blueprint, request, jsonify
from user_token import service as token_service

bp = Blueprint('token', __name__, url_prefix='/token')

@bp.route('/', methods=['GET'])
def get_tokens():
    return jsonify({"message": "Token list"})

@bp.route('/create', methods=['POST'])
def create():
    return jsonify({})

@bp.route('/update', methods=['PATCH'])
def update():
    return jsonify({})

@bp.route('/delete', methods=['DELETE'])
def delete():
    return jsonify({})