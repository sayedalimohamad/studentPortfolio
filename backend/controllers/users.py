from flask import Blueprint, request, jsonify
from extensions import db
from models import User

def register_routes(bp: Blueprint):
    @bp.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        user = User(
            username=data['username'],
            email=data['email'],
            role=data['role'],
            status='active'
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201

    @bp.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())

    @bp.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
        user.status = data.get('status', user.status)
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return jsonify(user.to_dict())

    @bp.route('/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204