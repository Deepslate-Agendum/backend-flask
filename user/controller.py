from flask import Blueprint, jsonify, request
import user.service as user_service
from user_token import service as token_service

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=['GET'])
def get_users():
    return jsonify({"message": "User list"})

@bp.route('/register', methods=['POST'])
def register():
    return jsonify({})

@bp.route('/update', methods=['POST'])
def update():
    return jsonify({})

@bp.route('/login', methods=['POST'])
def login():
    return jsonify({})

@bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({})