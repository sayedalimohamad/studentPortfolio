from flask import Blueprint, request, jsonify
from extensions import db
from models import Admin, User

def register_routes(bp: Blueprint):
    @bp.route('/admins', methods=['POST'])
    def create_admin():
        data = request.get_json()
        user = User(
            username=data['username'],
            email=data['email'],
            role='admin',
            status='active'
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        admin = Admin(
            user_id=user.user_id,
            created_by=data['created_by'],
            permissions=data['permissions'],
            role=data['role']
        )
        db.session.add(admin)
        db.session.commit()

        return jsonify(admin.to_dict()), 201

    @bp.route('/admins/<int:admin_id>', methods=['GET'])
    def get_admin(admin_id):
        admin = Admin.query.get_or_404(admin_id)
        return jsonify(admin.to_dict())

    @bp.route('/admins/<int:admin_id>', methods=['PUT'])
    def update_admin(admin_id):
        data = request.get_json()
        admin = Admin.query.get_or_404(admin_id)
        admin.permissions = data.get('permissions', admin.permissions)
        admin.role = data.get('role', admin.role)
        db.session.commit()
        return jsonify(admin.to_dict())

    @bp.route('/admins/<int:admin_id>', methods=['DELETE'])
    def delete_admin(admin_id):
        admin = Admin.query.get_or_404(admin_id)
        db.session.delete(admin)
        db.session.commit()
        return '', 204
    
     # Test route
    @bp.route('/test', methods=['GET'])
    def test():
        return "<h1>Admin blueprint is working!</h1>"