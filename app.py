from flask import Flask, jsonify
from api import api as api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

@app.route("/", methods=["GET"])
def hello_world():
	json_payload = "Hello from the Agendum REST API"
	return jsonify({"message": json_payload})

if __name__ == "__main__":
	app.run()