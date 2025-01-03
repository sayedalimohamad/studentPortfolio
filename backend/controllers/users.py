from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from . import users_bp


@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(
        username=data.get("username"),
        email=data.get("email"),
        role=data.get("role", "student"),
    )
    user.set_password(data.get("password"))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if user and user.check_password(data.get("password")):
        access_token = create_access_token(
            identity=user.user_id, additional_claims={"role": user.role}
        )
        return jsonify(access_token=access_token, role=user.role), 200
    return jsonify({"error": "Invalid credentials"}), 401


@users_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(user.to_dict()), 200


