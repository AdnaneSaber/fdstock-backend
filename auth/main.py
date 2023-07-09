from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from datetime import datetime, timedelta
import uuid
from models import User
from db import users_collection
from flask_cors import cross_origin
from dotenv import load_dotenv
import os
load_dotenv()

secret_key = os.getenv('SECRET_KEY')


auth_bp = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, secret_key)
            current_user = User(
                public_id=data['public_id'],
                name='',
                email='',
                password=''
            )
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@auth_bp.route('/login/', methods=['POST'])
@cross_origin()
def login():
    if request.method == 'OPTIONS':
        # Handle preflight request
        headers = {
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Max-Age': '86400',  # 24 hours
        }
        return ('', 204, headers)
    else:
        # creates dictionary of form data
        auth = request.json
        email = auth.get('email')
        password = auth.get('password')
        if not auth or not email and not password:
            # returns 401 if any email or / and password is missing
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
            )

        user = users_collection.find_one({
            "email": email
        })
        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            )

        if check_password_hash(user['password'], password):
            # generates the JWT Token
            token = jwt.encode({
                'public_id': user['public_id'],
                'exp': datetime.utcnow() + timedelta(weeks=36)
            }, secret_key)
            return make_response(jsonify({'token': token, "email": email, "user_id": user['public_id'], "name": user['name'], "username": user['username'], "ability": [
                {
                    "action": 'manage',
                    "subject": 'all'
                }
            ]}), 201)
        # returns 403 if password is wrong
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
        )


@auth_bp.route('/signup/', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.json

    # gets name, email and password
    name, email, username = data.get('name'), data.get(
        'email'), data.get('username')
    password = data.get('password')

    # checking for existing user
    user = users_collection.find_one({
        "email": email
    })
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        # insert user
        users_collection.insert_one(user.to_dict())

        return make_response({"email": email, "name": name, "password": password, "username": username, "ability": [
            {
                "action": 'manage',
                "subject": 'all'
            }
        ]}, 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)
