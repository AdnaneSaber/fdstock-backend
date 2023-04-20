from flask import Flask, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import shutil


# def jsonify(data):
#     return json.dumps(data)


app = Flask(__name__)
cors = CORS(app)
app.config["MONGO_URI"] = "mongodb+srv://hamzatalhaweb7:hamza00@cluster0.sodhv1g.mongodb.net/PFE?retryWrites=true&w=majority"
app.config['CORS_HEADERS'] = 'Content-Type'
mongo = PyMongo(app)

# Create to select all images from mongoDB database and return them as json
# [{'_id': ObjectId('6435dc1f11876970be800740'), 'image': {'id': '1', 'compressed': 'https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg', 'original': 'https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg', 'author': 'hamza', 'exif': 'girl, flowers, asian', 'downloads': '1', 'hasFace': True}, 'download': '1', 'view': '1'}]


@app.route('/images/', methods=['GET'])
@cross_origin()
def get_images():
    images = mongo.db.images
    output = []
    for image in images.find():
        output.append(
            {"download": image["download"], "view": image["view"], "image": image["image"]})
    return jsonify(output)


@app.route('/images/<id>', methods=['GET'])
def get_image(id):
    images = mongo.db.images
    output = []
    for image in images.find({"image.id": id}):
        output.append(
            {"download": image["download"], "view": image["view"], "image": image["image"]})
    return jsonify(output)


@app.route('/images/count/', methods=['GET'])
def get_images_count():
    images = mongo.db.images
    return jsonify({"count": images.count_documents({})})


@app.route('/disk/', methods=['GET'])
@cross_origin()
def get_disk():
    total, used, free = shutil.disk_usage("/")
    total = round(total / (2**30), 1)
    used = round(used / (2**30), 1)
    free = round(free / (2**30), 1)
    percentage = round(used / total * 100, 1)
    return jsonify({"total": f'{total}GB', "used": f'{used}GB', "free": f'{free}GB', 'percentage': percentage})


@app.route('/images/test', methods=['GET'])
@cross_origin()
def create_image_test():
    images = mongo.db.images
    images.insert_one({"image": {"id": "1", "compressed": "https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg",
                      "original": "https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg", "author": "hamza", "exif": "girl, flowers, asian", "downloads": "1", "hasFace": True}, "download": "1", "view": "1"})
    return jsonify({'message': 'image created'})


if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port="8000"
    )
