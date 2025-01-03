from flask import request, jsonify
from models import db, Event
from . import events_bp


@events_bp.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])


@events_bp.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    new_event = Event(**data)
    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict()), 201


@events_bp.route("/events/<int:id>", methods=["PUT"])
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(event, key, value)
    db.session.commit()
    return jsonify(event.to_dict())


@events_bp.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"}), 200
