from flask import request, jsonify
from models import db, Student
from . import students_bp


@students_bp.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])


@students_bp.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()
    new_student = Student(**data)
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201


@students_bp.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    return jsonify(student.to_dict())


@students_bp.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"}), 200
