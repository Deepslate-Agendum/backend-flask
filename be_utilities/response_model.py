from flask import jsonify


def known_error_response(message: str, type: str):
    return response(status="error", status_message=message,
                    status_type=type, http_response_code=400)
def unknown_error_response():
    return response(status="error", status_message="An unknown error occurred.",
                    status_type="unknown", http_response_code=500)
def success_response(message: str, object: object | list, object_name: str | list= None):
    if not isinstance(object, list) and isinstance(object_name, str):
        return response(status="success", http_response_code=200, objects=[object], object_names=[object_name])
    elif isinstance(object, list) and isinstance(object_name, str):
        return response(status="success", http_response_code=200, objects=[object], object_names=[object_name])
    elif isinstance(object, list) and isinstance(object_name, list):
        if len(object) != len(object_name):
            raise ValueError("Length mismatch: when providing multiple keys and objects, their lengths must match.")
        return response(status="success", http_response_code=200, objects=object, object_names=object_name)

def response(status: str, http_response_code: int, objects: list = None, object_names: list = None, status_message: str = None, status_type: str = None):
    if status != "error":
        response_dict = {"status" : status}
        if objects is not None and object_names is not None:
            for key, value in zip(object_names, objects):
                response_dict[key] = value
        return jsonify(response_dict), http_response_code
    else:
        return jsonify({
            "status": status,
            status : {
                "message": status_message,
                "type": status_type
            }
        }), http_response_code