from flask import Blueprint, request, jsonify
from extensions import db
from models import Student

def register_routes(bp: Blueprint):
    @bp.route('/students', methods=['POST'])
    def create_student():
        data = request.get_json()
        student = Student(
            user_id=data['user_id'],
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

    @bp.route('/students/<int:student_id>', methods=['GET'])
    def get_student(student_id):
        student = Student.query.get_or_404(student_id)
        return jsonify(student.to_dict())

    @bp.route('/students/<int:student_id>', methods=['PUT'])
    def update_student(student_id):
        data = request.get_json()
        student = Student.query.get_or_404(student_id)
        student.full_name = data.get('full_name', student.full_name)
        student.dob = data.get('dob', student.dob)
        student.institution = data.get('institution', student.institution)
        student.major = data.get('major', student.major)
        student.privacy_level = data.get('privacy_level', student.privacy_level)
        student.bio = data.get('bio', student.bio)
        db.session.commit()
        return jsonify(student.to_dict())

    @bp.route('/students/<int:student_id>', methods=['DELETE'])
    def delete_student(student_id):
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return '', 204