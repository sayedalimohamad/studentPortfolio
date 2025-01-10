from flask import Blueprint, request, jsonify
from extensions import db
from models import Event
from flask_jwt_extended import jwt_required, get_jwt_identity

def register_routes(bp: Blueprint):
    @bp.route('/', methods=['POST'])
    @jwt_required()
    def create_event():
        current_user = get_jwt_identity()
        data = request.get_json()
        event = Event(
            user_id=current_user,
            title=data['title'],
            description=data['description'],
            date=data['date'],
            location=data['location']
        )
        db.session.add(event)
        db.session.commit()
        return jsonify(event.to_dict()), 201

    @bp.route('/<int:event_id>', methods=['GET'])
    def get_event(event_id):
        event = Event.query.get_or_404(event_id)
        return jsonify(event.to_dict())

    @bp.route('/<int:event_id>', methods=['PUT'])
    @jwt_required()
    def update_event(event_id):
        event = Event.query.get_or_404(event_id)
        current_user = get_jwt_identity()
        if event.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        data = request.get_json()
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.date = data.get('date', event.date)
        event.location = data.get('location', event.location)
        db.session.commit()
        return jsonify(event.to_dict())

    @bp.route('/<int:event_id>', methods=['DELETE'])
    @jwt_required()
    def delete_event(event_id):
        event = Event.query.get_or_404(event_id)
        current_user = get_jwt_identity()
        if event.user_id != current_user:
            return jsonify({"error": "Unauthorized"}), 403

        db.session.delete(event)
        db.session.commit()
        return '', 204
    
    @bp.route('/test', methods=['GET'])
    def test():
        return "<h1>Events blueprint is working!</h1>"