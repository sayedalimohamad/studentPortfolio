from flask import Blueprint, request, jsonify
from extensions import db
from models import Student
from flask_jwt_extended import jwt_required, get_jwt_identity

def register_routes(bp: Blueprint):
    @bp.route('/', methods=['POST'])
    @jwt_required()
    def create_student():
        current_user = get_jwt_identity()
        data = request.get_json()
        student = Student(
            user_id=current_user,
            full_name=data['full_name'],
            dob=data['dob'],
            institution=data['institution'],
            major=data['major'],
            privacy_level=data['privacy_level'],
            bio=data.get('bio')
        )
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201
    
    @bp.route('/', methods=['GET'])
    def get_students():
        students = Student.query.all()
        return jsonify([student.to_dict() for student in students])

    @bp.route('/<int:student_id>', methods=['GET'])
    def get_student(student_id):
        student = Student.query.get_or_404(student_id)
        return jsonify(student.to_dict())

    @bp.route('/<int:student_id>', methods=['PUT'])
    @jwt_required()
    def update_student(student_id):
        student = Student.query.get_or_404(student_id)
        current_user = get_jwt_identity()
        if student.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()
        student.full_name = data.get('full_name', student.full_name)
        student.dob = data.get('dob', student.dob)
        student.institution = data.get('institution', student.institution)
        student.major = data.get('major', student.major)
        student.privacy_level = data.get('privacy_level', student.privacy_level)
        student.bio = data.get('bio', student.bio)
        db.session.commit()
        return jsonify(student.to_dict())

    @bp.route('/<int:student_id>', methods=['DELETE'])
    @jwt_required()
    def delete_student(student_id):
        student = Student.query.get_or_404(student_id)
        current_user = get_jwt_identity()
        if student.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        db.session.delete(student)
        db.session.commit()
        return '', 204