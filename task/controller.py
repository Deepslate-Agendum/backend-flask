from flask import Blueprint, jsonify, request
import task.service as task_service

bp = Blueprint('task', __name__, url_prefix='/task')

@bp.route('/create', methods=['POST'])
def create():
    name = request.json["name"]
    description = request.json["description"]
    tags = request.json["tags"]
    workspace_id = request.json["workspace_id"]
    due_date = request.json["due_date"]

    task_id = task_service.create(name, description, tags, workspace_id, due_date)
    if task_id >= 0:
        return jsonify({"task.id": task_id})
    else:
        return jsonify({"error": "Create task failed"}), 500

@bp.route('/', methods=['GET'])
@bp.route('/<int:id>', methods=['GET'])
def get_tasks(task_id: int = None):
    tasks = task_service.get(task_id)

    if tasks is not None:
        return jsonify({"tasks": tasks}), 200
    else:
        return jsonify({"error": "Task not found"}), 404

@bp.route('/update', methods=['PUT'])
def update():
    task_id = request.json["id"]
    name = request.json["name"]
    description = request.json["description"]
    tags = request.json["tags"]
    workspace_id = request.json["workspace_id"]
    due_date = request.json["due_date"]

    if task_service.update(task_id, name, description, tags, workspace_id, due_date):
        return "Success", 200
    else:
        return jsonify({"error": "Task not found"}), 404

@bp.route('/delete', methods=['DELETE'])
def delete():
    task_id = request.json["id"]

    if task_service.delete(task_id):
        return "Success", 200
    else:
        return jsonify({"error": "Task not found"}), 404