from flask import Blueprint, make_response, request
from db import users_collection, friendships_collection
from .functions import get_user, get_users_friends_ids, get_recommended_friends, get_people_list
from functions import get_user_from_token
from dotenv import load_dotenv
import os
load_dotenv()

secret_key = os.getenv('SECRET_KEY')


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile/<user_id>', methods=['POST'])
def get_profile_with_id(user_id):
    if user_id != "undefined":
        data = request.json
        token = data.get('token')
        if get_user_from_token(token, secret_key):
            user = get_user(user_id, users_collection)
            return make_response(user)
        else:
            return make_response({})
    else:
        return make_response({})


@profile_bp.route('/profile/<user_id>/friends_ids', methods=['POST'])
def get_friends(user_id):
    data = request.json
    token = data.get('token')
    if get_user_from_token(token, secret_key):
        friends = get_users_friends_ids(
            user_id, friendships_collection)
        return make_response(friends)
    else:
        return make_response({})


@profile_bp.route('/profile/<user_id>/recommended', methods=['POST'])
def get_recommended_friends(user_id):
    data = request.json
    token = data.get('token')
    if get_user_from_token(token, secret_key):
        friends = get_recommended_friends(
            user_id, friendships_collection)
        return make_response(friends)
    else:
        return make_response({})


@profile_bp.route('/profiles', methods=['POST'])
def get_prople():
    data = request.json
    token = data.get('token')
    if get_user_from_token(token, secret_key):
        friends = get_people_list(users_collection)
        return make_response(friends)
    else:
        return make_response({})