from flask import Blueprint

admin_bp = Blueprint("admin", __name__)
api_bp = Blueprint("api", __name__)
events_bp = Blueprint("events", __name__)
files_bp = Blueprint("files", __name__)
notifications_bp = Blueprint("notifications", __name__)
students_bp = Blueprint("students", __name__)
supervisors_bp = Blueprint("supervisors", __name__)
users_bp = Blueprint("users", __name__)

from . import admins, api, events, files, notifications, students, supervisors, users
