from flask import Blueprint
from user.controller import bp as user_bp
from task.controller import bp as task_bp
from workspace.controller import workspaces_bp, workspace_bp
from dependency.controller import blueprint as dependency_bp

api = Blueprint('api', __name__, url_prefix='/api')
api.register_blueprint(task_bp)
api.register_blueprint(user_bp)

workspace_bp.register_blueprint(dependency_bp)
api.register_blueprint(workspaces_bp)
