from . import main
from flask import request, jsonify

from web_app.db.models import Events

# CRUD for Events

@main.route('/events/all')
def get_events():
    events = [event.to_dict() for event in Events.get_all()]
    return jsonify(events)

@main.route('/events/<int:id>')
def get_event():
    if event := Events.get_by_id(id): # Get object event
        return jsonify(event.to_dict())
    return {'detail': 'Event not found.'}, 400

@main.route('/events/new', methods=['POST'])
def create_event():
    form = request.json # get data from form
    event = Events.create(form) # Create new event object
    if event.id:
        return {'detail': 'Event created succesfully'}
    return {'detail': 'Something went wrong. Try again later'}

@main.route('/events/<int:id>', methods=['PATCH'])
def update_event():
    data_to_update = request.json # Get data from fetch
    if event := Events.get_by_id(id): # Get object event
        event.update(data_to_update) # Update event
        return {'detail': 'User updated succesfully.'}
    return {'detail': 'Event not found.'}, 404

@main.route('/events/<int:id>', methods=['DELETE'])
def remove_event():
    if event := Events.get_by_id(id): # Get object event
        event.delete() # Remove event
        return {'detail': 'Event removed succesfully.'}
    return {'detail': 'Event not found.'}, 404