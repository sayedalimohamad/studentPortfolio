from flask import Blueprint, request, jsonify
from extensions import db
from models import Student
from flask_jwt_extended import jwt_required, get_jwt_identity


def register_routes(bp: Blueprint):
    @bp.route("/", methods=["GET"])
    def get_students():
        students = Student.query.all()
        return jsonify([student.to_dict() for student in students])

    @bp.route("/<int:student_id>", methods=["GET"])
    @jwt_required()
    def get_student(student_id):
        student = Student.query.get_or_404(student_id)
        return jsonify(student.to_dict())

    @bp.route("/<int:student_id>", methods=["PUT"])
    @jwt_required()
    def update_student(student_id):
        data = request.get_json()
        student = Student.query.get_or_404(student_id)
        current_user = get_jwt_identity()
        if student.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403
        student.institution = data.get("institution", student.institution)
        student.major = data.get("major", student.major)
        student.bio = data.get("bio", student.bio)
        student.privacy_level= data.get("privacy_level", student.privacy_level)
        db.session.commit()
        return jsonify(student.to_dict())

    @bp.route("/<int:student_id>", methods=["DELETE"])
    @jwt_required()
    def delete_student(student_id):
        student = Student.query.get_or_404(student_id)
        current_user = get_jwt_identity()
        if student.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403
        db.session.delete(student)
        db.session.commit()
        return "", 204

