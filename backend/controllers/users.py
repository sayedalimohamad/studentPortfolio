import socket
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from extensions import db
from models import User
from marshmallow import Schema, fields, ValidationError
import smtplib
from email.mime.text import MIMEText


def get_ip4_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True)


user_schema = UserSchema()


def send_password_reset_email(email, token):
    # Dynamically get the local IP address
    ip_address = get_ip4_address()
    reset_url = f"http://{ip_address}:3000/reset-password?token={token}"  # Assuming your frontend runs on port 3000

    msg = MIMEText(f"Click the link to reset your password: {reset_url}")
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = 'noreply@yourapp.com'
    msg['To'] = email

    # Use a local SMTP server or update to use your mail server settings
    with smtplib.SMTP('localhost', 1025) as server:
        server.sendmail('noreply@yourapp.com', [email], msg.as_string())


def register_routes(bp: Blueprint):
    @bp.route('/register', methods=['POST'])
    def create_user():
        try:
            data = user_schema.load(request.get_json())
            
            if User.query.filter_by(email=data['email']).first():
                return jsonify({"error": "Email already exists"}), 400
            
            if User.query.filter_by(username=data['username']).first():
                return jsonify({"error": "Username already exists"}), 400
            
            user = User(
                username=data['username'],
                email=data['email'],
                role=data['role'],
                status='active'
            )
            
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
            
            return jsonify(user.to_dict()), 201
        except ValidationError as err:
            return jsonify({"error": err.messages}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @bp.route('/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            user = User.query.filter_by(email=data['email']).first()
            
            if user and user.check_password(data['password']):
                access_token = create_access_token(identity=str(user.user_id))
                return jsonify(access_token=access_token, role=user.role), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @bp.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        jti = get_jwt()['jti']
        # Add the token to a blacklist (e.g., Redis or database)
        # blacklist.add(jti)
        return jsonify({"message": "Logged out successfully"}), 200

    @bp.route('/reset-password', methods=['POST'])
    def reset_password():
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        token = create_access_token(identity=str(user.user_id))
        send_password_reset_email(user.email, token)
        return jsonify({"message": "Password reset email sent"}), 200

    @bp.route('/me', methods=['GET'])
    @jwt_required()
    def get_current_user():
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @bp.route('/', methods=['GET'])
    @jwt_required()
    def get_users():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        users = User.query.paginate(page=page, per_page=per_page)
        return jsonify({
            "users": [user.to_dict() for user in users.items],
            "total": users.total,
            "pages": users.pages,
            "current_page": users.page
        })

    @bp.route('/<int:user_id>', methods=['GET'])
    @jwt_required()
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @bp.route('/<int:user_id>', methods=['PUT'])
    @jwt_required()
    def update_user(user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
        user.status = data.get('status', user.status)
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return jsonify(user.to_dict())

    @bp.route('/<int:user_id>', methods=['DELETE'])
    @jwt_required()
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
