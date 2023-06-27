from flask import Flask, jsonify, request, send_from_directory, flash, Response, url_for
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from typing import List
import shutil
import os
from functions import filter_request
from api import handleImage


app = Flask(__name__)
cors = CORS(app, resources={r'/*': {"origins": '*'}})
app.config["MONGO_URI"] = "mongodb+srv://hamzatalhaweb7:hamza00@cluster0.sodhv1g.mongodb.net/PFE?retryWrites=true&w=majority"
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = 'uploads'
mongo = PyMongo(app)

# Create to select all images from mongoDB database and return them as json
# [{'_id': ObjectId('6435dc1f11876970be800740'), 'image': {'id': '1', 'compressed': 'https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg', 'original': 'https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg', 'author': 'hamza', 'exif': 'girl, flowers, asian', 'downloads': '1', 'hasFace': True}, 'download': '1', 'view': '1'}]
images = mongo.db.images
browsers = mongo.db.browsers


@app.route('/imagesapi/<path:path>')
def _(path):
    return send_from_directory('images', path)


@app.route('/', methods=['GET'])
@cross_origin()
def get_images():
    output = []
    # needs to be sorted
    for image in images.find():
        del image['_id']
        output.append(image)
    return jsonify(output)


@app.route('/images/<id>', methods=['GET'])
def get_image(id):
    output = []
    for image in images.find({"id": id}):
        del image['_id']
        output.append(image)
    return jsonify(output)


@app.route("/images/search", methods=["GET"])
def search_images():
    gallery = request.args.get("gallery", type=bool, default=True)
    limitstart = request.args.get("limitstart", type=int, default=0)
    limitend = request.args.get("limitend", type=int, default=60)
    hasNoFace = request.args.get("hasNoFace")
    q = request.args.get("q", type=str, default="")
    orderby = request.args.get("orderby", type=str, default="RAND()")

    query = {"exif": {"$regex": q}}
    if not q:
        query = {}
    if hasNoFace != "false":
        query['hasFace'] = False
    projection = {"_id": 0}  # Exclude _id field from the result

    image_data = images.find(query, projection).sort(
        orderby).skip(limitstart).limit(limitend)
    image_data = list(image_data)

    return jsonify(image_data)


@app.route("/images/count", methods=["GET"])
def get_image_count():
    gallery = request.args.get("gallery", type=bool, default=True)
    q = request.args.get("q", type=str, default="")

    query = {"exif": {"$regex": q}}
    if not q:
        query = {}

    count = images.count_documents(query)

    return jsonify({"count": count})


@app.route('/images/download/<id>', methods=['POST'])
def add_download(id):
    images.update_one(filter={"id": id}, update={'$inc': {'downloads': 1}})
    return ""


@app.route('/images/view/<id>', methods=['POST'])
def add_view(id):
    browser = filter_request(request)
    browsers.update_one(filter={"key": browser}, update={'$inc': {'value': 1}})
    images.update_one(filter={"id": id}, update={'$inc': {'views': 1}})
    return ""


@app.route('/images/count/', methods=['GET'])
def get_images_count():
    return jsonify({"count": images.count_documents({})})

# create route to upload image to mongoDB database


UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/images/upload/', methods=['POST'])
def upload_image():
    allowed_files_to_upload: List[FileStorage] = []
    exifs = request.form.get('exif')
    for f in request.files:
        file = request.files.get(f)
        if file and allowed_file(file.filename):

            allowed_files_to_upload.append(file)
        else:
            return Response({"message": "Invalid file"}, status=400, mimetype='application/json')
    for el in allowed_files_to_upload:
        filename = secure_filename(el.filename)
        el.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = handleImage(filename, exifs)
        images.insert_one(data)
    return Response(status=200, mimetype='application/json')


@app.route('/disk/', methods=['GET'])
@cross_origin()
def get_disk():
    total, used, free = shutil.disk_usage("/")
    total = round(total / (2**30), 1)
    used = round(used / (2**30), 1)
    free = round(free / (2**30), 1)
    percentage = round(used / total * 100, 1)
    return jsonify({"total": f'{total}GB', "used": f'{used}GB', "free": f'{free}GB', 'percentage': percentage})


@app.route('/browserstats/', methods=['GET'])
@cross_origin()
def get_browser_stats():
    output = []
    B = browsers.find()
    count = 0
    for a in B:
        del a['_id']
        count += a['value']
        output.append(a)
    for el in output:
        el['value'] = int(el['value']) / count
    output.append({
        "key": "count", "value": count
    })
    return jsonify(output)


@app.route('/images/allviews', methods=['GET'])
@cross_origin()
def get_all_views():
    output = []
    for image in images.find():
        output.append(
            {"download": image["download"], "view": image["view"], "image": image["image"]})
    return jsonify(output)


@app.route('/images/test', methods=['GET'])
@cross_origin()
def create_image_test():
    images.insert_one({"image": {"id": "1", "compressed": "https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg",
                      "original": "https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg", "author": "hamza", "exif": "girl, flowers, asian", "downloads": "1", "hasFace": True}, "download": "1", "view": "1"})
    return jsonify({'message': 'image created'})


if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port="8000"
    )
