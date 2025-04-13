from flask import jsonify


def validation_error_response(message: str):
    return response(status="error", status_message=message,
                    status_type="validation", http_response_code=400)
def unknown_error_response(message: str):
    return response(status="error", status_message=message,
                    status_type="unknown", http_response_code=500)
def request_error_response(message: str):
    return response(status="error", status_message=message,
                    status_type="request", http_response_code=500)
def success_response(message: str, object = None):
    return response(status="success", status_message=message, status_type="object", http_response_code=200, object=object)

def response(status: str, status_message: str, status_type: str, http_response_code: int, object = None):
    if object != None:
        return jsonify({
        "status": status,
        status : {
            "message": status_message,
            "type": status_type
        },
        "object" : object
    }), http_response_code
    else:
        return jsonify({
            "status": status,
            status : {
                "message": status_message,
                "type": status_type
            }
        }), http_response_code