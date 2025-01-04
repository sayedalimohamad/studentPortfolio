from flask import Blueprint, request, jsonify
from extensions import db
from models import Notification

def register_routes(bp: Blueprint):
    @bp.route('/notifications', methods=['POST'])
    def create_notification():
        data = request.get_json()
        notification = Notification(
            user_id=data['user_id'],
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
    def delete_notification(notification_id):
        notification = Notification.query.get_or_404(notification_id)
        db.session.delete(notification)
        db.session.commit()
        return '', 204