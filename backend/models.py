from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)  
    full_name = db.Column(db.String(255), nullable=False)  
    dob = db.Column(db.Date, nullable=False)  
    created_at = db.Column(db.TIMESTAMP, default=db.func.now())
    last_login = db.Column(db.TIMESTAMP, default=db.func.now())
    status = db.Column(db.String(255), nullable=False)

    
    student = db.relationship("Student", backref="user", uselist=False, cascade="all, delete-orphan")
    supervisor = db.relationship("Supervisor", backref="user", uselist=False, cascade="all, delete-orphan")
    admin = db.relationship("Admin", backref="user", uselist=False, cascade="all, delete-orphan", foreign_keys="Admin.user_id")
    files = db.relationship("File", backref="user", cascade="all, delete-orphan")
    events = db.relationship("Event", backref="user", cascade="all, delete-orphan")
    notifications = db.relationship("Notification", backref="user", cascade="all, delete-orphan")
    history = db.relationship("History", backref="user", cascade="all, delete-orphan")
    recommendations = db.relationship("Recommendation", backref="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "full_name": self.full_name,
            "dob": self.dob,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "status": self.status
        }

class Student(db.Model):
    __tablename__ = "students"
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique=True)
    institution = db.Column(db.String(255), nullable=False)
    major = db.Column(db.String(255), nullable=False)
    privacy_level = db.Column(db.String(255), db.ForeignKey("privacy_levels.level"), nullable=False)
    bio = db.Column(db.Text)

    def to_dict(self):
        student_dict = {
            "student_id": self.student_id,
            "user_id": self.user_id,
            "institution": self.institution,
            "major": self.major,
            "privacy_level": self.privacy_level,
            "bio": self.bio
        }
        
        if self.user:
            student_dict.update({
                "full_name": self.user.full_name,
                "dob": self.user.dob,
                "email": self.user.email,
                "username": self.user.username,
            })
        return student_dict

class Supervisor(db.Model):
    __tablename__ = "supervisors"
    supervisor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique=True)
    institution = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)

    def to_dict(self):
        return {
            "supervisor_id": self.supervisor_id,
            "user_id": self.user_id,
            "institution": self.institution,
            "department": self.department,
            "bio": self.bio
        }

class Admin(db.Model):
    __tablename__ = "admins"
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    permissions = db.Column(db.JSON, nullable=False)
    role = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "admin_id": self.admin_id,
            "user_id": self.user_id,
            "created_by": self.created_by,
            "permissions": self.permissions,
            "role": self.role
        }

class File(db.Model):
    __tablename__ = "files"
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(255), nullable=False)
    file_type_id = db.Column(db.Integer, db.ForeignKey("file_types.file_type_id"))
    visibility = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.TIMESTAMP, default=db.func.now())

    def to_dict(self):
        return {
            "file_id": self.file_id,
            "user_id": self.user_id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "file_type_id": self.file_type_id,
            "visibility": self.visibility,
            "uploaded_at": self.uploaded_at
        }

class History(db.Model):
    __tablename__ = "history"
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    action_type = db.Column(db.String(255), nullable=False)
    action_details = db.Column(db.String(255), nullable=False)
    entity_type = db.Column(db.String(255), db.ForeignKey("entity_types.type"), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=db.func.now())

    def to_dict(self):
        return {
            "history_id": self.history_id,
            "user_id": self.user_id,
            "action_type": self.action_type,
            "action_details": self.action_details,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "timestamp": self.timestamp
        }

class Event(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.now())

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "location": self.location,
            "created_at": self.created_at
        }

class Recommendation(db.Model):
    __tablename__ = "recommendations"
    recommendation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"))
    recommended_at = db.Column(db.TIMESTAMP, default=db.func.now())
    status = db.Column(db.String(255), db.ForeignKey("recommendation_status.status"), nullable=False)

    def to_dict(self):
        return {
            "recommendation_id": self.recommendation_id,
            "user_id": self.user_id,
            "event_id": self.event_id,
            "recommended_at": self.recommended_at,
            "status": self.status
        }

class Notification(db.Model):
    __tablename__ = "notifications"
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.now())

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "message": self.message,
            "created_at": self.created_at
        }

class PrivacyLevel(db.Model):
    __tablename__ = "privacy_levels"
    level = db.Column(db.String(255), primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "level": self.level,
            "description": self.description
        }

class FileType(db.Model):
    __tablename__ = "file_types"
    file_type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "file_type_id": self.file_type_id,
            "type_name": self.type_name
        }

class EntityType(db.Model):
    __tablename__ = "entity_types"
    type = db.Column(db.String(255), primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "type": self.type,
            "description": self.description
        }

class RecommendationStatus(db.Model):
    __tablename__ = "recommendation_status"
    status = db.Column(db.String(255), primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "status": self.status,
            "description": self.description
        }