import json

from flask import Blueprint, jsonify, request
import task.service as task_service

bp = Blueprint('task', __name__, url_prefix='/task')

# HACK: serialize task
def serialize_task(task):
    fields = {
        "id": task.id.binary.hex(),
        "dependencies": [dependency.pk.binary.hex() for dependency in task.dependencies],
    }
    tags = []
    for field_value in task.nonstatic_field_values:
        if field_value.field.name == "Name":
            fields.update({"title": field_value.value})
        if field_value.field.name == "Description":
            fields.update({"description": field_value.value})
        if field_value.field.value_type.name == "Tag":
            tags.append(field_value.field.name)
        if field_value.field.name == "Due Date":
            fields.update({"due_date": field_value.value})
        if field_value.field.name == "X Location":
            fields.update({"x_location": field_value.value})
        if field_value.field.name == "Y Location":
            fields.update({"y_location": field_value.value})
    fields.update({"tags": tags})

    return fields

@bp.route('/create', methods=['POST'])
def create():
    name = request.json["name"]
    description = request.json["description"]
    tags = request.json["tags"]
    workspace_id = request.json["workspace_id"]
    due_date = request.json["due_date"]
    x_location = request.json.get("x_location", "0")
    y_location = request.json.get("y_location", "0")

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
    name = request.json["name"]
    description = request.json["description"]
    tags = request.json["tags"]
    workspace_id = request.json["workspace_id"]
    due_date = request.json["due_date"]
    x_location = request.json.get("x_location", 0.0)
    y_location = request.json.get("y_location", 0.0)

    if task_service.update(task_id, workspace_id, name, description, tags, due_date, x_location, y_location):
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