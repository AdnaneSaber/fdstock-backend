from flask import Blueprint, jsonify, request, make_response
from db import events_collection
from flask_cors import cross_origin
from .functions import create_event, delete_event, read_all_events, read_event, update_event
from dotenv import load_dotenv
import os
load_dotenv()

secret_key = os.getenv('SECRET_KEY')


events_bp = Blueprint('events', __name__)

# Create an event


@events_bp.route('/calendar/add-event', methods=['POST'])
def create_event_view():
    data = request.get_json()
    event_data = {
        **data['event'],
        "user": data["user_id"]
    }
    event_id = create_event(event_data, events_collection)
    return jsonify({'event_id': event_id}), 201

# Read an event


# @events_bp.route('/events/<event_id>', methods=['GET'])
# def read_event_view(event_id):
#     event = read_event(event_id, events_collection)
#     if event:
#         return jsonify(event)
#     else:
#         return jsonify({'message': 'Event not found'}), 404

# Update an event


@events_bp.route('/calendar/update-event', methods=['PUT'])
def update_event_view():
    data = request.get_json()
    updated_data = data['event']
    print(updated_data)
    if update_event(updated_data['id'], updated_data, events_collection):
        return jsonify({'message': 'Event updated'})
    else:
        return jsonify({'message': 'Event not found'}), 404

# Delete an event


@events_bp.route('/calendar/remove-event/<event_id>', methods=['DELETE'])
def delete_event_view(event_id):
    print(event_id)
    if delete_event(event_id, events_collection):
        return jsonify({'message': 'Event deleted'})
    else:
        return jsonify({'message': 'Event not found'}), 404

# Read all events for a user


@events_bp.route('/calendar/events/user/<user_id>', methods=['POST'])
def read_all_events_view(user_id):
    data = request.get_json()
    calendars = data['calendars']
    print(calendars)
    events = read_all_events(user_id, calendars, events_collection)
    return events
