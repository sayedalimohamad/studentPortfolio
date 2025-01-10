from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from extensions import db, jwt, cors, migrate
from controllers import (
    admin_bp,
    api_bp,
    events_bp,
    files_bp,
    notifications_bp,
    students_bp,
    supervisors_bp,
    users_bp,
)
import os
import socket

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    # Register Blueprints
    app.register_blueprint(admin_bp, url_prefix="/api/admins")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(events_bp, url_prefix="/api/events")
    app.register_blueprint(files_bp, url_prefix="/api/files")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(students_bp, url_prefix="/api/students")
    app.register_blueprint(supervisors_bp, url_prefix="/api/supervisors")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


def get_ip4_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000, host=f"{get_ip4_address()}")