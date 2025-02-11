from flask import Blueprint, jsonify, request
import task.service as task_service

bp = Blueprint('task', __name__, url_prefix='/task')

@bp.route('/create', methods=['POST'])
def create():
    return jsonify({})

@bp.route('/', methods=['GET'])
def get_tasks():
    return jsonify({"message": "Task List"})

@bp.route('/update', methods=['POST'])
def update():
    return jsonify({})

@bp.route('/delete', methods=['POST'])
def delete():
    return jsonify({})