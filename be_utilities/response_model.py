from flask import jsonify


def known_error_response(message: str, type: str):
    return response(status="error", status_message=message,
                    status_type=type, http_response_code=400)
def unknown_error_response():
    return response(status="error", status_message="An unknown error occurred.",
                    status_type="unknown", http_response_code=500)
def success_response(message: str, object = None, object_name: str = None):
    return response(status="success", status_message=message, status_type="object", http_response_code=200, object=object, object_name=object_name)

def response(status: str, status_message: str, status_type: str, http_response_code: int, object = None, object_name: str = None):
    if status != "error" and object != None:
        return jsonify({
        "status": status,
        object_name : object
    }), http_response_code
    else:
        return jsonify({
            "status": status,
            status : {
                "message": status_message,
                "type": status_type
            }
        }), http_response_code