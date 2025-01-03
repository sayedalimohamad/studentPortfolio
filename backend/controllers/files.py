from flask import request, jsonify
from models import db, File
from . import files_bp


@files_bp.route("/files", methods=["GET"])
def get_files():
    files = File.query.all()
    return jsonify([file.to_dict() for file in files])


@files_bp.route("/files", methods=["POST"])
def upload_file():
    data = request.get_json()
    new_file = File(**data)
    db.session.add(new_file)
    db.session.commit()
    return jsonify(new_file.to_dict()), 201


@files_bp.route("/files/<int:id>", methods=["PUT"])
def update_file(id):
    file = File.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(file, key, value)
    db.session.commit()
    return jsonify(file.to_dict())


@files_bp.route("/files/<int:id>", methods=["DELETE"])
def delete_file(id):
    file = File.query.get_or_404(id)
    db.session.delete(file)
    db.session.commit()
    return jsonify({"message": "File deleted"}), 200
