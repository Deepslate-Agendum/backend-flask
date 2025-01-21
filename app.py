from flask import Flask, jsonify

app = Flask(__name__)

_json_payload = "Hello from the Agendum REST API"

@app.route("/", methods=["GET"])
def hello_world():
	return jsonify({"message": _json_payload})

if __name__ == "__main__":
	app.run()