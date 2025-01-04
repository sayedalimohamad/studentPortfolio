from flask import Blueprint, request, jsonify
from extensions import db
from models import Event

def register_routes(bp: Blueprint):
    @bp.route('/events', methods=['POST'])
    def create_event():
        data = request.get_json()
        event = Event(
            user_id=data['user_id'],
            title=data['title'],
            description=data['description'],
            date=data['date'],
            location=data['location']
        )
        db.session.add(event)
        db.session.commit()
        return jsonify(event.to_dict()), 201

    @bp.route('/events/<int:event_id>', methods=['GET'])
    def get_event(event_id):
        event = Event.query.get_or_404(event_id)
        return jsonify(event.to_dict())

    @bp.route('/events/<int:event_id>', methods=['PUT'])
    def update_event(event_id):
        data = request.get_json()
        event = Event.query.get_or_404(event_id)
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.date = data.get('date', event.date)
        event.location = data.get('location', event.location)
        db.session.commit()
        return jsonify(event.to_dict())

    @bp.route('/events/<int:event_id>', methods=['DELETE'])
    def delete_event(event_id):
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return '', 204
    
    # test route
    @bp.route('/test', methods=['GET'])
    def test():
        return "<h1>Events blueprint is working!</h1>"