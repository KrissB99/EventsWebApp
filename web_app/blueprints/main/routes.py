from datetime import datetime
from . import main
from flask import request, jsonify, session

from web_app.db.models import Events, UsersOnEvents, Logs

@main.after_request
def log_status_code(response):
    Logs.new(request.path, response.status_code)
    return response

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
    form['author_id'] = session['user_id']
    event = Events.create(form) # Create new event object
    if event.id:
        return {'detail': 'Event created succesfully'}
    return {'detail': 'Something went wrong. Try again later'}

@main.route('/events/<int:id>', methods=['PATCH'])
def update_event(id:int):
    data_to_update = request.json # Get data from fetch
    if event := Events.get_by_id(id): # Get object event
        for date in ['date_from', 'date_to']:
            data_to_update[date] = datetime.strptime(data_to_update[date], "%Y-%m-%d")
        event.update(data_to_update) # Update event
        return {'detail': 'Event updated succesfully.'}
    return {'detail': 'Event not found.'}, 404

@main.route('/events/<int:id>', methods=['DELETE'])
def remove_event(id:int):
    if event := Events.get_by_id(id): # Get object event
        event.delete() # Remove event
        return {'detail': 'Event removed succesfully.'}
    return {'detail': 'Event not found.'}, 404

# CRUD for UsersOnEvents

@main.route('/events/sign-up/<int:id>', methods=['POST'])
def create_relationship_user_event(id:int):
    data = request.json
    if Events.get_by_id(id):
        data['user_id'], data['event_id'] = session['user_id'], id
        UsersOnEvents.create(data)
        return {'detail': "You signed up for event!"}
    return {'detail': 'Event not found.'}, 404

@main.route('/events/update-attendance/<int:id>', methods=['PATCH'])
def update_relationship_user_event(id:int):
    data_to_update = request.json 
    if relationship := UsersOnEvents.get_by_id(id):
        relationship.update(data_to_update)
        return {'detail': 'Atendance on event updated.'}
    return {'detail': 'Event not found'}, 400

@main.route('/events/resign/<int:id>', methods=['DELETE'])
def remove_relationship_user_event(id:int):
    if relationship := UsersOnEvents.get_by_id(id):
        relationship.delete()
        return {'detail': 'Atendance on event updated.'}
    return {'detail': 'Event not found'}, 400
