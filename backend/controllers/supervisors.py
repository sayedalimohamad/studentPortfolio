from flask import Blueprint, request, jsonify
from extensions import db
from models import Supervisor, User
from flask_jwt_extended import jwt_required, get_jwt_identity


def register_routes(bp: Blueprint):
    @bp.route("/", methods=["GET"])
    def get_supervisors():
        supervisors = (
            db.session.query(Supervisor, User)
            .join(User, Supervisor.user_id == User.user_id)
            .all()
        )
        result = []
        for supervisor, user in supervisors:
            supervisor_data = supervisor.to_dict()
            supervisor_data["user"] = user.to_dict()
            result.append(supervisor_data)
        return jsonify(result)

    @bp.route("/<int:supervisor_id>", methods=["GET"])
    @jwt_required()
    def get_supervisor(supervisor_id):
        supervisor, user = (
            db.session.query(Supervisor, User)
            .join(User, Supervisor.user_id == User.user_id)
            .filter(Supervisor.supervisor_id == supervisor_id)
            .first_or_404()
        )
        supervisor_data = supervisor.to_dict()
        supervisor_data["user"] = user.to_dict()
        return jsonify(supervisor_data)

    @bp.route("/<int:supervisor_id>", methods=["PUT"])
    @jwt_required()
    def update_supervisor(supervisor_id):
        data = request.get_json()
        supervisor = Supervisor.query.get_or_404(supervisor_id)
        current_user_id = get_jwt_identity()
        if supervisor.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        supervisor.institution = data.get("institution", supervisor.institution)
        supervisor.department = data.get("department", supervisor.department)
        supervisor.bio = data.get("bio", supervisor.bio)
        db.session.commit()
        return jsonify(supervisor.to_dict())

    @bp.route("/<int:supervisor_id>", methods=["DELETE"])
    @jwt_required()
    def delete_supervisor(supervisor_id):
        supervisor = Supervisor.query.get_or_404(supervisor_id)
        current_user_id = get_jwt_identity()
        if supervisor.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
        db.session.delete(supervisor)
        db.session.commit()
        return "", 204

   