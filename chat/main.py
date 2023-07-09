import datetime
from flask_socketio import SocketIO, join_room, leave_room, emit
from db import messages_collection
from flask import Blueprint, make_response, jsonify, request
from functions import get_user_from_token
from dotenv import load_dotenv
from .functions import get_last_conversations, get_unseen_messages, read_unseen_messages, get_messages_with, read_message
import os
load_dotenv()

secret_key = os.getenv('SECRET_KEY')
chat_bp = Blueprint('chat', __name__)
socketio = SocketIO(cors_allowed_origins="*")
# SOCKETIO


@socketio.on('connect')
def handle_connect():
    # Handle connection time and last logged etc
    print('Client connected')


@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    print(f'User joined room: {room}')


@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    print(f'User left room: {room}')


@socketio.on('private_message')
def handle_private_message(data):
    message = data['message']
    recipient = data['recipient']
    token = data['token']
    sender = get_user_from_token(token, secret_key)
    # Create a unique room name for the private message
    sorted_strings = sorted([recipient, sender])
    room = "-".join(sorted_strings)

    join_room(room)
    # leave_room(room)

    # Store the message in the database
    message_doc = {
        'sender': sender,
        'recipient': recipient,
        'message': message,
        'timestamp': str(datetime.datetime.now()),
        'deleted': False,
        'edited': False,
        'seen': False,
        'old_message': None
    }
    message = messages_collection.insert_one(message_doc)
    message_id = str(message.inserted_id)
    
    emit('private_message', {**message_doc, '_id': message_id}, room=room)

@chat_bp.route('/messages', methods=['POST'])
def last_converstaions():
    data = request.json
    token = data.get('token')
    user_id = get_user_from_token(token, secret_key)
    if user_id:
        conversations = get_last_conversations(user_id, messages_collection)
        return make_response(conversations)
    else:
        return make_response(jsonify([]))


@chat_bp.route('/unseen', methods=['POST'])
def unseen_messages():
    data = request.json
    token = data.get('token')
    user_id = get_user_from_token(token, secret_key)
    if user_id:
        unseen_messages = get_unseen_messages(user_id, messages_collection)
        return make_response(unseen_messages)
    else:
        return make_response(jsonify([]))


@chat_bp.route('/read_all', methods=['POST'])
def read_all_messages():
    data = request.json
    token = data.get('token')
    user_id = get_user_from_token(token, secret_key)
    if user_id:
        unseen_messages = read_unseen_messages(user_id, messages_collection)
        return make_response(unseen_messages)
    else:
        return make_response(jsonify([]))


@chat_bp.route('/messages/<chat_with>', methods=['POST'])
def read_all_messages_with(chat_with):
    data = request.json
    token = data.get('token')
    user_id = get_user_from_token(token, secret_key)
    if user_id:
        messages = get_messages_with(
            user_id, chat_with,  messages_collection)
        return make_response(messages)
    else:
        return make_response(jsonify([]))

@chat_bp.route('/message/read/<message_id>/<user2_id>', methods=['POST'])
def read_message_view(message_id, user2_id):
    data = request.json
    token = data.get('token')
    user_id = get_user_from_token(token, secret_key)
    if user_id:
        read_message(user_id, user2_id, message_id, messages_collection)
        return make_response(jsonify([]))
    else:
        return make_response(jsonify([]))


def init_socketio_app(app):
    socketio.init_app(app)
