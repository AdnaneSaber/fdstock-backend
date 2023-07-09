from flask import Blueprint
from pymongo import MongoClient
import os

db_bp = Blueprint('db', __name__)
db_key = os.getenv('db')


class Database:
    def __init__(self):
        self.client = MongoClient(db_key)
        self.db = self.client['PFE']

    def get_collection(self, collection_name):
        return self.db[collection_name]


db = Database()
images_collection = db.get_collection("images")
browsers_collection = db.get_collection("browsers")
users_collection = db.get_collection("users")
messages_collection = db.get_collection("messages")
friendships_collection = db.get_collection("friendships")
events_collection = db.get_collection("events")
