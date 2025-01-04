import os
from dotenv import load_dotenv

# Load environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'instance', 'student_portfolio.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key")

    # File Uploads
    UPLOAD_FOLDER = os.path.join(basedir, "uploads")
    ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Debugging
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # CORS
    CORS_HEADERS = 'Content-Type'

    # Additional configurations
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True