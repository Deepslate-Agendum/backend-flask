from flask import Blueprint, jsonify, request
import task.service as task_service
from be_utilities.util_funcs import get_param_from_body as body
from be_utilities.util_funcs import get_param_from_url as url
from be_utilities.util_funcs import KNOWN_EXCEPTIONS
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
        name = body(request, "name")
        description = body(request, "description")
        tags = body(request, "tags")
        workspace_id = body(request, "workspace_id")
        due_date = body(request, "due_date")
        x_location = body(request, "x_location", 0.0)
        y_location = body(request, "y_location", 0.0)
        return responses.success_response("create_task",
            serialize_task(task_service.create(workspace_id, name, description, tags, due_date, x_location, y_location)), object_name="task")
    except KNOWN_EXCEPTIONS as e:
        return responses.known_error_response(str(e), type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()


@bp.route('/', methods=['GET'])
@bp.route('/<string:task_id>', methods=['GET'])
def get_tasks(task_id: int = None):
    try:
        workspace_id = url(request, "workspace_id")
        tasks = task_service.get(task_id, workspace_id)

        # HACK: same deal as in user
        if isinstance(tasks, list):
            tasks_json = [serialize_task(task) for task in tasks]
        else:
            tasks_json = serialize_task(tasks)
        return responses.success_response("get_tasks", tasks_json, object_name="tasks")
    except KNOWN_EXCEPTIONS as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@bp.route('/update', methods=['PUT'])
def update():
    try:
        task_id = body(request, "id")
        name = body(request, "name")
        description = body(request, "description")
        tags = body(request, "tags")
        workspace_id = body(request, "workspace_id")
        due_date = body(request, "due_date")
        x_location = body(request, "x_location", 0.0)
        y_location = body(request, "y_location", 0.0)
        task_service.update(task_id, workspace_id, name, description, tags, due_date, x_location, y_location)
        return responses.success_response("update_task")
    except KNOWN_EXCEPTIONS as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response()

@bp.route('/delete', methods=['DELETE'])
def delete():
    try:
        task_id = body(request, "id")
        task_service.delete(task_id)
        return responses.success_response(message="delete_task")
    except KNOWN_EXCEPTIONS as e:
        return responses.known_error_response(message=str(e), type=type(e).__name__)
    except Exception as e:
        return responses.unknown_error_response(e)