from .service_exceptions import ServiceException
from db_python_util.db_exceptions import DBException
from werkzeug.exceptions import BadRequest
def get_param_from_body(request, param_name, default = None):
    try:
        if default == None:
            return request.json[param_name]
        else:
            return request.json.get(param_name, default)
    except KeyError:
        raise KeyError(f"Missing {param_name} in request JSON body.")
    except BadRequest:
        raise BadRequest(f"{param_name} is malformed in the request JSON body.")
def get_param_from_url(request, param_name):
    try:
        return request.args[param_name]
    except KeyError:
        raise KeyError(f"Missing {param_name} in request URL arguments.")

KNOWN_EXCEPTIONS = (KeyError, BadRequest, DBException, ServiceException)