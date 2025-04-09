from flask import Flask
from .auth_routes import auth_blueprint
from .user_routes import user_blueprint
from .project_routes import project_blueprint
from .task_routes import task_blueprint

def create_app():
    app = Flask(__name__)

    # Register Blueprints with the main app
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(project_blueprint, url_prefix='/project')
    app.register_blueprint(task_blueprint, url_prefix='/task')

    return app