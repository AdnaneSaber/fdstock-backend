
from helpers import CustomJSONEncoder
import json
from bson import ObjectId


def get_last_conversations(user_id, messages_collection):
    pipeline = [
        # Match messages where the user is the sender or recipient
        {
            '$match': {
                '$or': [
                    {'sender': user_id},
                    {'recipient': user_id}
                ]
            }
        },
        # Sort by the latest message timestamp
        {'$sort': {'timestamp': -1}},
        # Group messages by the other participant
        {
            '$group': {
                '_id': {
                    '$cond': [
                        {'$eq': ['$sender', user_id]},
                        '$recipient',
                        '$sender'
                    ]
                },
                'last_message': {'$first': '$message'},
                'last_timestamp': {'$first': '$timestamp'}
            }
        },
        # Lookup the sender data from the users collection
        {
            '$lookup': {
                'from': 'users',
                'localField': '_id',
                'foreignField': 'public_id',
                'as': 'sender'
            }
        },
        {
            '$lookup': {
                'from': 'messages',
                'let': {'senderId': '$_id', 'recipientId': user_id},
                'pipeline': [
                    {
                        '$match': {
                            '$expr': {
                                '$and': [
                                    {'$eq': ['$sender', '$$senderId']},
                                    {'$eq': ['$recipient', '$$recipientId']},
                                    {'$eq': ['$seen', False]}
                                ]
                            }
                        }
                    },
                    {
                        '$count': 'unseen_messages'
                    }
                ],
                'as': 'unseen_messages'
            }
        },
        # Project the count of unseen messages for each sender
        {
            '$project': {
                '_id': 1,
                'sender': {
                    '$cond': [
                        {'$isArray': '$sender'},
                        {
                            '$let': {
                                'vars': {'sender': {'$arrayElemAt': ['$sender', 0]}},
                                'in': {
                                    '_id': '$$sender.public_id',
                                    'name': '$$sender.name',
                                    'username': '$$sender.username',
                                }
                            }
                        },
                        '$sender'
                    ]
                },
                'last_message': 1,
                'last_timestamp': 1,
                'unseen_messages': {'$arrayElemAt': ['$unseen_messages.unseen_messages', 0]}
            }
        }
    ]

    last_conversations = list(messages_collection.aggregate(pipeline))
    serialized_messages = json.dumps(
        list(last_conversations), cls=CustomJSONEncoder)
    return serialized_messages


def get_unseen_messages(user_id, messages_collection):
    pipeline = [
        {
            '$match': {
                'recipient': user_id,
                'seen': False
            }
        },
        {
            '$lookup': {
                'from': 'users',
                'localField': 'sender',
                'foreignField': 'public_id',
                'as': 'sender'
            }
        },
        {
            '$project': {
                '_id': 1,
                'sender': {
                    '$cond': [
                        {'$isArray': '$sender'},
                        {
                            '$let': {
                                'vars': {'sender': {'$arrayElemAt': ['$sender', 0]}},
                                'in': {
                                    '_id': '$$sender.public_id',
                                    'name': '$$sender.name',
                                    'username': '$$sender.username',
                                }
                            }
                        },
                        '$sender'
                    ]
                },
                'message': 1,
                'timestamp': 1,
                'deleted': 1
            }
        }
    ]

    unseen_messages = list(messages_collection.aggregate(pipeline))
    serialized_messages = json.dumps(
        list(unseen_messages), cls=CustomJSONEncoder)
    return serialized_messages


def read_unseen_messages(user_id, messages_collection):
    filter = {
        'recipient': user_id,
        'seen': False
    }
    update = {
        '$set': {'seen': True}
    }
    unseen_messages = list(messages_collection.find(filter))
    serialized_messages = json.dumps(
        list(unseen_messages), cls=CustomJSONEncoder)
    messages_collection.update_many(filter, update)
    return serialized_messages


def get_messages_with(user_id, chat_with, messages_collection):
    # Define the query to retrieve the messages
    query = {
        '$or': [
            {'sender': user_id, 'recipient': chat_with},
            {'sender': chat_with, 'recipient': user_id}
        ]
    }
    messages = list(messages_collection.find(query).sort('timestamp', 1))
    serialized_messages = json.dumps(
        list(messages), cls=CustomJSONEncoder)
    return serialized_messages


def read_message(user_id, user2_id, message_id, messages_collection):
    filter = {
        'recipient': user_id,
        'sender': user2_id,
        '_id': ObjectId(message_id),
        'seen': False
    }
    update = {
        '$set': {'seen': True}
    }
    messages = list(messages_collection.find(filter))
    print(filter)
    print(messages)
    serialized_messages = json.dumps(
        list(messages), cls=CustomJSONEncoder)
    messages_collection.update_many(filter, update)
    print(serialized_messages)
    return serialized_messages
