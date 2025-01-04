from flask import Blueprint, request, jsonify
from extensions import db
from models import Supervisor

def register_routes(bp: Blueprint):
    @bp.route('/supervisors', methods=['POST'])
    def create_supervisor():
        data = request.get_json()
        supervisor = Supervisor(
            user_id=data['user_id'],
            institution=data['institution'],
            department=data['department'],
            bio=data.get('bio')
        )
        db.session.add(supervisor)
        db.session.commit()
        return jsonify(supervisor.to_dict()), 201

    @bp.route('/supervisors/<int:supervisor_id>', methods=['GET'])
    def get_supervisor(supervisor_id):
        supervisor = Supervisor.query.get_or_404(supervisor_id)
        return jsonify(supervisor.to_dict())

    @bp.route('/supervisors/<int:supervisor_id>', methods=['PUT'])
    def update_supervisor(supervisor_id):
        data = request.get_json()
        supervisor = Supervisor.query.get_or_404(supervisor_id)
        supervisor.institution = data.get('institution', supervisor.institution)
        supervisor.department = data.get('department', supervisor.department)
        supervisor.bio = data.get('bio', supervisor.bio)
        db.session.commit()
        return jsonify(supervisor.to_dict())

    @bp.route('/supervisors/<int:supervisor_id>', methods=['DELETE'])
    def delete_supervisor(supervisor_id):
        supervisor = Supervisor.query.get_or_404(supervisor_id)
        db.session.delete(supervisor)
        db.session.commit()
        return '', 204