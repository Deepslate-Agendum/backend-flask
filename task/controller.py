import json

from flask import Blueprint, jsonify, request
from task.field_manager import FieldManager
import task.service as task_service

bp = Blueprint('task', __name__, url_prefix='/task')

# HACK: serialize task
def serialize_task(task):
    field_manager = FieldManager(task)

    dependencies = [dependency.pk.binary.hex() for dependency in task.dependencies]
    title = field_manager.get_field_value("Name", 0)
    description = field_manager.get_field_value("Description", 0)
    due_date = field_manager.get_field_value("Due Date", 0)
    status = field_manager.get_field_value("Status", 0).value
    x_location = float(field_manager.get_field_value("X Location", 0))
    y_location = float(field_manager.get_field_value("Y Location", 0))
    tags = [tag.value for tag in field_manager.get_field_values("Tags")]

    fields = {
        "id": task.id.binary.hex(),
        "dependencies": dependencies,
        "title": title,
        "description": description,
        "due_date": due_date,
        "status": status,
        "x_location": x_location,
        "y_location": y_location,
        "tags": tags,
    }

    return fields

@bp.route('/create', methods=['POST'])
def create():
    name = request.json["title"]
    description = request.json["description"]
    tags = request.json["tags"]
    workspace_id = request.json["workspace_id"]
    due_date = request.json["due_date"]
    x_location = request.json.get("x_location", 0.0)
    y_location = request.json.get("y_location", 0.0)

    task = task_service.create(workspace_id, name, description, tags, due_date, x_location, y_location)
    if task is not None:
        return jsonify(serialize_task(task)), 200
    else:
        return jsonify({"error": "Create task failed"}), 500

@bp.route('/', methods=['GET'])
@bp.route('/<int:task_id>', methods=['GET'])
def get_tasks(task_id: int = None):
    workspace_id = request.args['workspace_id']

    tasks = task_service.get(task_id, workspace_id)

    # HACK: same deal as in user
    if isinstance(tasks, list):
        tasks_json = [serialize_task(task) for task in tasks]
    else:
        tasks_json = serialize_task(tasks)

    return jsonify({'tasks': tasks_json}), 200

@bp.route('/update', methods=['PUT'])
def update():
    task_id = request.json["id"]
    name = request.json.get("title")
    description = request.json.get("description")
    tags = request.json.get("tags")
    workspace_id = request.json.get("workspace_id")
    due_date = request.json.get("due_date")
    x_location = request.json.get("x_location")
    y_location = request.json.get("y_location")
    status = request.json.get("status")

    if task_service.update(task_id, workspace_id, name, description, tags, due_date, x_location, y_location, status):
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