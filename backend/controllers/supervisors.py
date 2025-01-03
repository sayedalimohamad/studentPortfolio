from flask import request, jsonify
from models import db, Supervisor
from . import supervisors_bp


@supervisors_bp.route("/supervisors", methods=["GET"])
def get_supervisors():
    supervisors = Supervisor.query.all()
    return jsonify([supervisor.to_dict() for supervisor in supervisors])


@supervisors_bp.route("/supervisors", methods=["POST"])
def create_supervisor():
    data = request.get_json()
    new_supervisor = Supervisor(**data)
    db.session.add(new_supervisor)
    db.session.commit()
    return jsonify(new_supervisor.to_dict()), 201


@supervisors_bp.route("/supervisors/<int:id>", methods=["PUT"])
def update_supervisor(id):
    supervisor = Supervisor.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(supervisor, key, value)
    db.session.commit()
    return jsonify(supervisor.to_dict())


@supervisors_bp.route("/supervisors/<int:id>", methods=["DELETE"])
def delete_supervisor(id):
    supervisor = Supervisor.query.get_or_404(id)
    db.session.delete(supervisor)
    db.session.commit()
    return jsonify({"message": "Supervisor deleted"}), 200
