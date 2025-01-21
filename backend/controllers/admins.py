from flask import Blueprint, request, jsonify
from extensions import db
from models import Admin, User
from flask_jwt_extended import jwt_required, get_jwt_identity


def register_routes(bp: Blueprint):
    @bp.route("/", methods=["GET"])
    def get_admins():
        admins = (
            db.session.query(Admin, User)
            .join(User, Admin.user_id == User.user_id)
            .all()
        )
        result = []
        for admin, user in admins:
            admin_data = admin.to_dict()
            admin_data["user"] = user.to_dict()
            result.append(admin_data)
        return jsonify(result)

    @bp.route("/<int:admin_id>", methods=["GET"])
    @jwt_required()
    def get_admin(admin_id):
        admin, user = (
            db.session.query(Admin, User)
            .join(User, Admin.user_id == User.user_id)
            .filter(Admin.admin_id == admin_id)
            .first_or_404()
        )
        admin_data = admin.to_dict()
        admin_data["user"] = user.to_dict()
        return jsonify(admin_data)

    @bp.route("/<int:admin_id>", methods=["PUT"])
    @jwt_required()
    def update_admin(admin_id):
        data = request.get_json()
        admin = Admin.query.get_or_404(admin_id)
        current_user_id = get_jwt_identity()
        if admin.created_by != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        admin.permissions = data.get("permissions", admin.permissions)
        admin.role = data.get("role", admin.role)
        db.session.commit()
        return jsonify(admin.to_dict())

    @bp.route("/<int:admin_id>", methods=["DELETE"])
    @jwt_required()
    def delete_admin(admin_id):
        admin = Admin.query.get_or_404(admin_id)
        current_user_id = get_jwt_identity()
        if admin.created_by != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        db.session.delete(admin)
        db.session.commit()
        return "", 204

    
