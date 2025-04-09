import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Flask Configuration Class"""

    # 🔐 Security Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SESSION_TYPE = 'filesystem'  # Use filesystem for storing session data

    # 📡 Database Configuration
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "project_management")
    DB_AUTH_PLUGIN = os.getenv("DB_AUTH_PLUGIN", "caching_sha2_password")

    # 📧 Email Configuration (For Password Reset)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # Email address
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # App-specific password
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    # 🔐 Security (Password Reset)
    PASSWORD_RESET_TOKEN_EXPIRATION = 3600  # Token expires in 1 hour

    # 🚀 Debug Mode (for Development)
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]

    @staticmethod
    def init_app(app):
        """Initialize Flask App with this config"""
        pass
