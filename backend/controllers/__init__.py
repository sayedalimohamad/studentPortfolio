from flask import Blueprint

# Initialize blueprints
admin_bp = Blueprint("admin", __name__)
api_bp = Blueprint("api", __name__)
events_bp = Blueprint("events", __name__)
files_bp = Blueprint("files", __name__)
notifications_bp = Blueprint("notifications", __name__)
students_bp = Blueprint("students", __name__)
supervisors_bp = Blueprint("supervisors", __name__)
users_bp = Blueprint("users", __name__)

try:
    from . import admins, api, events, files, notifications, students, supervisors, users
except ImportError as e:
    raise ImportError(f"Failed to import routes: {e}")

# Register the routes for each blueprint
try:
    admins.register_routes(admin_bp)
    api.register_routes(api_bp)
    events.register_routes(events_bp)
    files.register_routes(files_bp)
    notifications.register_routes(notifications_bp)
    students.register_routes(students_bp)
    supervisors.register_routes(supervisors_bp)
    users.register_routes(users_bp)
except Exception as e:
    raise RuntimeError(f"Failed to register routes: {e}")