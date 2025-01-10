from flask import Blueprint, request, jsonify
from extensions import db
from models import Notification
from flask_jwt_extended import jwt_required, get_jwt_identity

def register_routes(bp: Blueprint):
    @bp.route('/notifications', methods=['POST'])
    @jwt_required()
    def create_notification():
        current_user = get_jwt_identity()
        data = request.get_json()
        notification = Notification(
            user_id=current_user,
            message=data['message']
        )
        db.session.add(notification)
        db.session.commit()
        return jsonify(notification.to_dict()), 201

    @bp.route('/notifications/<int:notification_id>', methods=['GET'])
    def get_notification(notification_id):
        notification = Notification.query.get_or_404(notification_id)
        return jsonify(notification.to_dict())

    @bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
    @jwt_required()
    def delete_notification(notification_id):
        notification = Notification.query.get_or_404(notification_id)
        current_user = get_jwt_identity()
        if notification.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        db.session.delete(notification)
        db.session.commit()
        return '', 204