from bson import ObjectId
from helpers import CustomJSONEncoder
import json


def read_all_events(user_id, calendars, events_collection):
    events = events_collection.find({'user': user_id,
                                     'extendedProps.calendar': {'$in': calendars}
                                     })
    event_list = []
    for event in events:
        event['id'] = str(event['_id'])
        del event['_id']
        event_list.append(event)
    return json.dumps(list(event_list), cls=CustomJSONEncoder)


def create_event(event_data, events_collection):
    result = events_collection.insert_one(event_data)
    return str(result.inserted_id)


def read_event(event_id, events_collection):
    event = events_collection.find_one({'_id': ObjectId(event_id)})
    return event


def update_event(event_id, updated_data, events_collection):
    events_collection.update_one(
        {'_id': ObjectId(event_id)}, {'$set': updated_data})
    return True


def delete_event(event_id, events_collection):
    events_collection.delete_one({'_id': ObjectId(event_id)})
    return True
