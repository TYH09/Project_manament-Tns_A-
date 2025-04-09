from flask_session import Session

def init_session(app):
    """
    Initializes Flask session using the configuration from `config.py`.
    """
    Session(app)
