from flask import jsonify

SUCCESS_CODES = 200

def known_error_response(message: str, exception_type: str):
    return response(http_response_code=400, status_message=message, status_type=exception_type)
def unknown_error_response():
    return response(http_response_code=500, status_message="An unknown error occurred.", status_type="unknown")

def success_response(items: object | list, key: str = None):
    return response(http_response_code=200, items=items, item_key=key)

def response(http_response_code: int, items: list = None, item_key: str = None, status_message: str = None,
             status_type: str = None):
    if http_response_code == SUCCESS_CODES:
        # case 1: we got no object
        if items is None:
            return jsonify({}), http_response_code
        # case 2: if the object is by itself then just return it
        if not isinstance(items, list):
            return jsonify(items), http_response_code
        # case 3: if the object is a list, then require a key and return a keyed list
        if item_key is None:
            raise ValueError("A key must be provided when supplying a list of objects.")
        if not isinstance(item_key, str):
            raise ValueError("Object name must be a string when provided for a list of objects.")
        return jsonify({item_key: items}), http_response_code
    else:
        return jsonify({
            "message": status_message,
            "type": status_type
        }), http_response_code