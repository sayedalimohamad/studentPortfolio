from flask import request, jsonify
from models import db, Admin
from . import admin_bp


@admin_bp.route("/admins", methods=["GET"])
def get_admins():
    admins = Admin.query.all()
    return jsonify([admin.to_dict() for admin in admins])


@admin_bp.route("/admins", methods=["POST"])
def create_admin():
    data = request.get_json()
    new_admin = Admin(**data)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify(new_admin.to_dict()), 201


@admin_bp.route("/admins/<int:id>", methods=["PUT"])
def update_admin(id):
    admin = Admin.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(admin, key, value)
    db.session.commit()
    return jsonify(admin.to_dict())


@admin_bp.route("/admins/<int:id>", methods=["DELETE"])
def delete_admin(id):
    admin = Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin deleted"}), 200
