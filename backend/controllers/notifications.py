from flask import request, jsonify
from models import db, Notification
from . import notifications_bp


@notifications_bp.route("/notifications", methods=["GET"])
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([notification.to_dict() for notification in notifications])


@notifications_bp.route("/notifications", methods=["POST"])
def create_notification():
    data = request.get_json()
    new_notification = Notification(**data)
    db.session.add(new_notification)
    db.session.commit()
    return jsonify(new_notification.to_dict()), 201


@notifications_bp.route("/notifications/<int:id>", methods=["PUT"])
def update_notification(id):
    notification = Notification.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(notification, key, value)
    db.session.commit()
    return jsonify(notification.to_dict())


@notifications_bp.route("/notifications/<int:id>", methods=["DELETE"])
def delete_notification(id):
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted"}), 200
