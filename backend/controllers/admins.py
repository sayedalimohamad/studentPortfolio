from flask import Blueprint, request, jsonify
from extensions import db
from models import Admin, User

def register_routes(bp: Blueprint):
    @bp.route('/', methods=['POST'])
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
    
    @bp.route('/', methods=['GET'])
    def get_admins():
        # Join Admin and User tables to get all admin details
        admins = db.session.query(Admin, User).join(User, Admin.user_id == User.user_id).all()
        result = []
        for admin, user in admins:
            admin_data = admin.to_dict()
            admin_data['user'] = user.to_dict()  # Include user details
            result.append(admin_data)
        return jsonify(result)

    @bp.route('/<int:admin_id>', methods=['GET'])
    def get_admin(admin_id):
        # Join Admin and User tables to get details for a specific admin
        admin, user = db.session.query(Admin, User).join(User, Admin.user_id == User.user_id).filter(Admin.admin_id == admin_id).first_or_404()
        admin_data = admin.to_dict()
        admin_data['user'] = user.to_dict()  # Include user details
        return jsonify(admin_data)

    @bp.route('/<int:admin_id>', methods=['PUT'])
    def update_admin(admin_id):
        data = request.get_json()
        admin = Admin.query.get_or_404(admin_id)
        admin.permissions = data.get('permissions', admin.permissions)
        admin.role = data.get('role', admin.role)
        db.session.commit()
        return jsonify(admin.to_dict())

    @bp.route('/<int:admin_id>', methods=['DELETE'])
    def delete_admin(admin_id):
        admin = Admin.query.get_or_404(admin_id)
        db.session.delete(admin)
        db.session.commit()
        return '', 204
    
    # Test route
    @bp.route('/test', methods=['GET'])
    def test():
        return "<h1>Admin blueprint is working!</h1>"