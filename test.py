# in the file output.json loop through an array of objects and insert them into the mongoDB database.
import json
from pymongo import MongoClient
f = open("output.json", "r")
Mongo_server = "mongodb+srv://hamzatalhaweb7:hamza00@cluster0.sodhv1g.mongodb.net/PFE?retryWrites=true&w=majority"
data = json.load(f)
images = data['images']

# for image in images insert into mongoDB database
client = MongoClient(Mongo_server)
db = client.PFE
# collection = db.images
# for image in images:
#     # collection.delete_many({})
#     collection.insert_one(image)
# client.close()


B = ["Google Chrome",
     "Mozilla Firefox",
     "Apple Safari",
     "Internet Explorer",
     "Opera",
     "Microsoft Edge",
     "Unknown"]

browsers = db.browsers

browsers.delete_many({})
for browser in B:
    browsers.insert_one({"key": browser, "value": 0})
