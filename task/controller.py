from flask import Blueprint, jsonify, request
import task.service as task_service
from be_utilities.service_exceptions import ServiceException
import be_utilities.response_model as responses


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
    try:
        name = (request.json["name"])
        description = (request.json["description"])
        tags = request.json["tags"]
        workspace_id = (request.json["workspace_id"])
        due_date = request.json["due_date"]
        x_location = (request.json.get("x_location", "0"))
        y_location = (request.json.get("y_location", "0"))
    except KeyError as e:
        return responses.request_error_response(str(e))
    try:
        return responses.success_response("create_task",
            serialize_task(task_service.create(workspace_id, name, description, tags, due_date, x_location, y_location)), object_name="task")
    except ServiceException as e:
        return responses.known_error_response(str(e), e.__qualname__)
    except Exception as e:
        return responses.unknown_error_response(str(e), e.__qualname__)


@bp.route('/', methods=['GET'])
@bp.route('/<string:task_id>', methods=['GET'])
def get_tasks(task_id: int = None):
    try:
        workspace_id = (request.args['workspace_id'])
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        tasks = task_service.get(task_id, workspace_id)

        # HACK: same deal as in user
        if isinstance(tasks, list):
            tasks_json = [serialize_task(task) for task in tasks]
        else:
            tasks_json = serialize_task(tasks)
        return responses.success_response("get_tasks", tasks_json, object_name="tasks")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@bp.route('/update', methods=['PUT'])
def update():
    try:
        task_id = (request.json["id"])
        name = (request.json["name"])
        description = (request.json["description"])
        tags = request.json["tags"]
        workspace_id = (request.json["workspace_id"])
        due_date = request.json["due_date"]
        x_location = (request.json.get("x_location", 0.0))
        y_location = (request.json.get("y_location", 0.0))
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        task_service.update(task_id, workspace_id, name, description, tags, due_date, x_location, y_location)
        return responses.success_response("update_task")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        task_id = (request.json["id"])
    except KeyError as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    try:
        task_service.delete(task_id)
        return responses.success_response(message="delete_task")
    except ServiceException as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response(e)