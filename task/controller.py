from flask import Blueprint, jsonify, request
import task.service as task_service
from be_utilities.validation_exceptions import ValidationException
import be_utilities.response_model as responses


bp = Blueprint('task', __name__, url_prefix='/task')

# HACK: serialize task
def serialize_task(task):
    fields = {"id": task.id.binary.hex()}
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
        name = str(request.json["name"])
        description = str(request.json["description"])
        tags = request.json["tags"]
        workspace_id = str(request.json["workspace_id"])
        due_date = request.json["due_date"]
        x_location = str(request.json.get("x_location", "0"))
        y_location = str(request.json.get("y_location", "0"))
    except KeyError as e:
        return responses.request_error_response(e)
    try:
        return responses.success_response("create_task",
            serialize_task(task_service.create(workspace_id, name, description, tags, due_date, x_location, y_location)))
    except ValidationException as e:
        return responses.validation_error_response(e)
    except Exception as e:
        return responses.unknown_error_response(e)


@bp.route('/', methods=['GET'])
@bp.route('/<string:task_id>', methods=['GET'])
def get_tasks(task_id: int = None):
    try:
        workspace_id = str(request.args['workspace_id'])
    except KeyError as e:
        workspace_id = None
    try:
        tasks = task_service.get(task_id, workspace_id)

        # HACK: same deal as in user
        if isinstance(tasks, list):
            tasks_json = [serialize_task(task) for task in tasks]
        else:
            tasks_json = serialize_task(tasks)
        return responses.success_response("get_tasks", tasks_json)
    except ValidationException as e:
        return responses.validation_error_response(e)
    except Exception as e:
        return responses.unknown_error_response(e)

@bp.route('/update', methods=['PUT'])
def update():
    try:
        task_id = str(request.json["id"])
        name = str(request.json["name"])
        description = str(request.json["description"])
        tags = request.json["tags"]
        workspace_id = str(request.json["workspace_id"])
        due_date = request.json["due_date"]
        x_location = str(request.json.get("x_location", "0"))
        y_location = str(request.json.get("y_location", "0"))
    except KeyError as e:
        return responses.request_error_response(e)
    try:
        task_service.update(task_id, workspace_id, name, description, tags, due_date, x_location, y_location)
        return responses.success_response("update_task")
    except ValidationException as e:
        return responses.validation_error_response(e)
    except Exception as e:
        return responses.unknown_error_response(e)

@bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        task_id = str(request.json["id"])
    except KeyError as e:
        return responses.request_error_response(e)
    try:
        task_service.delete(task_id)
        return "Success", 200
    except ValidationException as e:
        return responses.validation_error_response(e)
    except Exception as e:
        return responses.unknown_error_response(e)