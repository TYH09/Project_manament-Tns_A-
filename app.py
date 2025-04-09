from flask import Flask
from routes.auth_routes import auth_blueprint
from routes.user_routes import user_blueprint
from routes.project_routes import project_blueprint
from db import get_db_connection
from config import Config
from custom_session.session import init_session
from routes.task_routes import task_blueprint




app = Flask(__name__)

# Load configuration from Config class
app.config.from_object(Config)

# Initialize session
init_session(app)

# Register each Blueprint individually
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(project_blueprint, url_prefix='/project')
app.register_blueprint(task_blueprint, url_prefix='/task')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])