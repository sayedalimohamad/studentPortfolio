from flask import Blueprint, request, jsonify
from extensions import db
from models import Event, Recommendation, User
from flask_jwt_extended import jwt_required, get_jwt_identity


def register_routes(bp: Blueprint):
    @bp.route("/", methods=["POST"])
    @jwt_required()
    def create_event():
        current_user = get_jwt_identity()
        data = request.get_json()
        event = Event(
            user_id=current_user,
            title=data["title"],
            description=data["description"],
            date=data["date"],
            location=data["location"],
        )
        db.session.add(event)
        db.session.commit()

        # Add a recommendation with 'pending' status
        recommendation = Recommendation(
            user_id=current_user, event_id=event.event_id, status="pending"
        )
        db.session.add(recommendation)
        db.session.commit()

        return jsonify(event.to_dict()), 201

    @bp.route("/", methods=["GET"])
    @jwt_required()
    def get_events():
        current_user = get_jwt_identity()
        user = User.query.get(current_user)

        if user.role == "student":
            # Show only 'accepted' events for students
            events = (
                Event.query.join(Recommendation)
                .filter(Recommendation.status == "accepted")
                .all()
            )
        else:
            # Show all events for admins/supervisors
            events = Event.query.all()

        # Include recommendation status in the response
        events_with_status = []
        for event in events:
            event_dict = event.to_dict()
            recommendation = Recommendation.query.filter_by(event_id=event.event_id).first()
            event_dict["status"] = recommendation.status if recommendation else "pending"
            events_with_status.append(event_dict)

        return jsonify(events_with_status)
    
    @bp.route("/<int:event_id>", methods=["PUT"])
    @jwt_required()
    def update_event(event_id):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)

        # Retrieve the event to ensure it exists
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404

        # Only allow the creator of the event or an admin/supervisor to update
        if user.role not in ["admin", "supervisor"] and event.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        # Update event details
        data = request.get_json()
        event.title = data.get("title", event.title)
        event.description = data.get("description", event.description)
        event.date = data.get("date", event.date)
        event.location = data.get("location", event.location)

        db.session.commit()

        return jsonify(event.to_dict()), 200


    @bp.route("/<int:event_id>/status", methods=["PUT"])
    @jwt_required()
    def update_recommendation_status(event_id):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)

        if user.role not in ["admin", "supervisor"]:
            return jsonify({"error": "Unauthorized"}), 403

        recommendation = Recommendation.query.filter_by(event_id=event_id).first()
        if not recommendation:
            return jsonify({"error": "Recommendation not found"}), 404

        data = request.get_json()
        new_status = data.get("status")
        if new_status not in ["pending", "accepted", "rejected"]:
            return jsonify({"error": "Invalid status"}), 400

        recommendation.status = new_status
        db.session.commit()

        return jsonify({"message": "Recommendation status updated"}), 200

    @bp.route("/<int:event_id>", methods=["DELETE"])
    @jwt_required()
    def delete_event(event_id):
        current_user = get_jwt_identity()
        user = User.query.get(current_user)

        # Retrieve the event to ensure it exists
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404

        # Only allow the creator of the event or an admin/supervisor to delete
        if user.role not in ["admin", "supervisor"] and event.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        # Delete associated recommendations first
        Recommendation.query.filter_by(event_id=event_id).delete()

        # Delete the event
        db.session.delete(event)
        db.session.commit()

        return jsonify({"message": "Event deleted successfully"}), 200

    @bp.route("/test", methods=["GET"])
    def test():
        return "<h1>Events blueprint is working!</h1>"
