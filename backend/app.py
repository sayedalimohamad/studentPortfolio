from flask import Flask, jsonify, request
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
from services.ai_service import ask_ai
from utils.auth import role_required, get_current_user_id
from models import Student

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register Blueprints
    app.register_blueprint(admin_bp, url_prefix="/api/admins")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(events_bp, url_prefix="/api/events")
    app.register_blueprint(files_bp, url_prefix="/api/files")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(students_bp, url_prefix="/api/students")
    app.register_blueprint(supervisors_bp, url_prefix="/api/supervisors")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    # Example route using AI service and auth utilities
    @app.route("/api/ask", methods=["POST"])
    @role_required("student")  # Protect the route
    def ask():
        data = request.get_json()
        question = data.get("question")
        user_id = get_current_user_id()  # Get the current user's ID
        response = ask_ai(question)  # Use the AI service
        return jsonify({"user_id": user_id, "response": response})
    
    @app.route("/api/students", methods=["GET"])
    # @role_required("supervisor")
    def get_students():
        students = Student.query.all()
        return jsonify([student.to_dict() for student in students])
    

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
