from flask import Flask, jsonify
from task.controller import bp as task_bp
from user.controller import bp as user_bp
from workspace.controller import bp as workspace_bp
from user_token.controller import bp as user_token_bp

app = Flask(__name__)
app.register_blueprint(task_bp)
app.register_blueprint(user_bp)
app.register_blueprint(workspace_bp)
app.register_blueprint(user_token_bp)


@app.route("/", methods=["GET"])
def hello_world():
	json_payload = "Hello from the Agendum REST API"
	return jsonify({"message": json_payload})

if __name__ == "__main__":
	app.run()