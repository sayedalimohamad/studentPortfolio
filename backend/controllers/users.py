import socket
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from extensions import db
from models import User, Admin, Supervisor, Student
from marshmallow import Schema, fields, ValidationError
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta


def get_ip4_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


def send_password_reset_email(email, token):
    ip_address = get_ip4_address()
    reset_url = f"http://{ip_address}:3000/reset-password?token={token}"
    msg = MIMEText(f"Click the link to reset your password: {reset_url}")
    msg["Subject"] = "Password Reset Request"
    msg["From"] = "noreply@yourapp.com"
    msg["To"] = email
    with smtplib.SMTP("localhost", 1025) as server:
        server.sendmail("noreply@yourapp.com", [email], msg.as_string())


class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True)
    full_name = fields.Str(required=True)
    dob = fields.Str(required=True)
    status = fields.Str(required=False)
    permissions = fields.Dict(required=False)
    created_by = fields.Str(required=False)
    institution = fields.Str(required=False)
    department = fields.Str(required=False)
    bio = fields.Str(required=False)
    major = fields.Str(required=False)
    privacy_level = fields.Str(required=False)


user_schema = UserSchema()


def register_routes(bp: Blueprint):
    @bp.route("/register", methods=["POST"])
    def create_user():
        try:
            data = user_schema.load(request.get_json())
            dob_date = datetime.strptime(data["dob"], "%Y-%m-%d").date()
            if User.query.filter_by(email=data["email"]).first():
                return jsonify({"error": "Email already exists"}), 400
            if User.query.filter_by(username=data["username"]).first():
                return jsonify({"error": "Username already exists"}), 400
            user = User(
                username=data["username"],
                email=data["email"],
                role=data["role"],
                full_name=data["full_name"],
                dob=dob_date,
                status="active",
            )
            user.set_password(data["password"])
            db.session.add(user)
            db.session.commit()
            if data["role"] == "admin":
                admin = Admin(
                    user_id=user.user_id,
                    permissions=data.get("permissions", {}),
                    created_by=data.get("created_by"),
                    role=data["role"],
                )
                db.session.add(admin)
            elif data["role"] == "supervisor":
                supervisor = Supervisor(
                    user_id=user.user_id,
                    institution=data.get("institution"),
                    department=data.get("department"),
                    bio=data.get("bio"),
                )
                db.session.add(supervisor)
            elif data["role"] == "student":
                student = Student(
                    user_id=user.user_id,
                    institution=data.get("institution"),
                    major=data.get("major"),
                    privacy_level=data.get("privacy_level"),
                    bio=data.get("bio"),
                )
                db.session.add(student)
            db.session.commit()
            return jsonify(user.to_dict()), 201
        except ValidationError as err:
            print("Validation Error:", err.messages)
            return jsonify({"error": "Validation error", "details": err.messages}), 400
        except Exception as e:
            print("Internal Server Error:", str(e))
            return jsonify({"error": "Internal server error", "details": str(e)}), 500

    @bp.route("/login", methods=["POST"])
    def login():
        try:
            data = request.get_json()
            user = User.query.filter_by(email=data["email"]).first()
            if user and user.check_password(data["password"]):
                access_token = create_access_token(identity=str(user.user_id), expires_delta=timedelta(hours=24))
                return jsonify(access_token=access_token, role=user.role), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @bp.route("/logout", methods=["POST"])
    @jwt_required()
    def logout():
        jti = get_jwt()["jti"]
        return jsonify({"message": "Logged out successfully"}), 200

    @bp.route("/reset-password", methods=["POST"])
    def reset_password():
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        token = create_access_token(identity=str(user.user_id))
        send_password_reset_email(user.email, token)
        return jsonify({"message": "Password reset email sent"}), 200

    @bp.route("/me", methods=["GET"])
    @jwt_required()
    def get_current_user():
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @bp.route("/", methods=["GET"])
    @jwt_required()
    def get_users():
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        users = User.query.paginate(page=page, per_page=per_page)
        return jsonify(
            {
                "users": [user.to_dict() for user in users.items],
                "total": users.total,
                "pages": users.pages,
                "current_page": users.page,
            }
        )

    @bp.route("/<int:user_id>", methods=["GET"])
    @jwt_required()
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @bp.route("/<int:user_id>", methods=["PUT"])
    @jwt_required()
    def update_user(user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)
        user.role = data.get("role", user.role)
        user.status = data.get("status", user.status)
        if "password" in data:
            user.set_password(data["password"])
        db.session.commit()
        return jsonify(user.to_dict())

    @bp.route("/<int:user_id>", methods=["DELETE"])
    @jwt_required()
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return "", 204
    
    @bp.route("/verify-password", methods=["POST"])
    @jwt_required()
    def verify_password():
        try:
            data = request.get_json()
            if not data or "password" not in data:
                return jsonify({"isValid": False, "message": "Password is required."}), 400
            
            user_id = get_jwt_identity()  # Get the user ID from the JWT token
            user = User.query.get(user_id)

            if not user:
                return jsonify({"isValid": False, "message": "User not found."}), 404

            # Verify the password
            if user.check_password(data["password"]):
                return jsonify({"isValid": True, "message": "Password is correct."}), 200
            else:
                return jsonify({"isValid": False, "message": "Incorrect password."}), 401

        except Exception as e:
            print("Error verifying password:", str(e))
            return jsonify({"isValid": False, "message": "Internal server error."}), 500
