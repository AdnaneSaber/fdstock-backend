
from helpers import CustomJSONEncoder
import json


def get_user(user_id, users_collection):
    user = users_collection.find_one({
        "public_id": user_id
    })
    return json.dumps(dict(user), cls=CustomJSONEncoder)


def get_users_friends_ids(user_id, friendship_collection):
    query = {
        '$or': [
            {'user1': user_id},
            {'user2': user_id}
        ],
        'status': 'accepted'
    }
    friends = friendship_collection.find(query)
    friend_ids = []
    for friend in friends:
        friend_id = friend['user1'] if friend['user2'] == user_id else friend['user2']
        friend_ids.append(friend_id)

    # Return the friend details
    return json.dumps(list(friend_ids), cls=CustomJSONEncoder)


def get_users_friends(user_id, friendship_collection, users_collection):
    # Define the query to retrieve the friends of the user
    query = {
        '$or': [
            {'user1': user_id},
            {'user2': user_id}
        ],
        'status': 'accepted'
    }

    # Retrieve the friends from the friendship collection
    friends = friendship_collection.find(query)

    # Extract the friend IDs from the friends' documents
    friend_ids = []
    for friend in friends:
        friend_id = friend['user1'] if friend['user2'] == user_id else friend['user2']
        friend_ids.append(friend_id)

    # Retrieve the friend details from the users collection
    friend_details = users_collection.find(
        {'public_id': {'$in': friend_ids}}, {'password': 0})

    # Return the friend details
    return json.dumps(list(friend_ids), cls=CustomJSONEncoder)


def send_friend_request(sender_id, recipient_id, friendship_collection):
    friendship_doc = {
        'user1': sender_id,
        'user2': recipient_id,
        'status': 'pending',
        'sender_id': sender_id
    }
    friendship_collection.insert_one(friendship_doc)


def get_recommended_friends(user_id, friendship_collection):
    pipeline = [
        {'$match': {'user_id': user_id}},  # Match user's friendships
        {'$lookup': {
            'from': 'friendships',
            'localField': 'friend_id',
            'foreignField': 'user_id',
            'as': 'friend_data'
        }},
        {'$unwind': '$friend_data'},
        {'$lookup': {
            'from': 'users',
            'localField': 'friend_data.friend_id',
            'foreignField': '_id',
            'as': 'friend_user_data'
        }},
        {'$unwind': '$friend_user_data'},
        {'$group': {
            '_id': '$friend_data.friend_id',
            'friend_count': {'$sum': 1},
            'friend_user_data': {'$first': '$friend_user_data'}
        }},
        {'$sort': {'friend_count': -1}},
        {'$limit': 5}  # Limit the number of recommendations
    ]

    recommended_friends = list(friendship_collection.aggregate(pipeline))
    return recommended_friends

def get_people_list(users_collection):
    return json.dumps(list(users_collection.find()), cls=CustomJSONEncoder)