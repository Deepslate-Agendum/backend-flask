from .controller_exceptions import MissingArgumentException
def get_param_from_body(request, param_name, default = None):
    try:
        if default == None:
            return request.json[param_name]
        else:
            return request.json.get(param_name, default)
    except KeyError:
        raise MissingArgumentException(f"Missing {param_name} in request JSON body.")
def get_param_from_url(request, param_name):
    try:
        return request.args[param_name]
    except KeyError:
        raise MissingArgumentException(f"Missing {param_name} in request URL arguments.")