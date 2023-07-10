
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from typing import List
import shutil
import os
from flask import Blueprint, jsonify, request, send_from_directory, Response
from .api import handleImage
import os
from functions import filter_request_agent
from db import images_collection, browsers_collection


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = "uploads"
images_bp = Blueprint('images_handler', __name__)


@images_bp.route('/imagesapi/<path:path>')
def _(path):
    return send_from_directory('images', path)


@images_bp.route('/', methods=['GET'])
@cross_origin()
def get_images():
    output = []
    # needs to be sorted
    for image in images_collection.find():
        del image['_id']
        output.append(image)
    return jsonify(output)


@images_bp.route('/images/<id>', methods=['GET'])
def get_image(id):
    output = []
    for image in images_collection.find({"id": id}):
        del image['_id']
        output.append(image)
    return jsonify(output)


@images_bp.route("/images/search", methods=["GET"])
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
    if hasNoFace == "true":
        query['hasFace'] = False
    elif hasNoFace == "false":
        query['hasFace'] = True
    
    
    projection = {"_id": 0}  # Exclude _id field from the result

    image_data = images_collection.find(query, projection).sort(
        orderby).skip(limitstart).limit(limitend)
    image_data = list(image_data)

    return jsonify(image_data)


@images_bp.route("/images/count", methods=["GET"])
def get_image_count():
    gallery = request.args.get("gallery", type=bool, default=True)
    q = request.args.get("q", type=str, default="")

    query = {"exif": {"$regex": q}}
    if not q:
        query = {}

    count = images_collection.count_documents(query)

    return jsonify({"count": count})


@images_bp.route('/images/download/<id>', methods=['POST'])
def add_download(id):
    images_collection.update_one(filter={"id": id}, update={
                                 '$inc': {'downloads': 1}})
    return ""


@images_bp.route('/images/view/<id>', methods=['POST'])
def add_view(id):
    browser = filter_request_agent(request)
    browsers_collection.update_one(
        filter={"key": browser}, update={'$inc': {'value': 1}})
    images_collection.update_one(
        filter={"id": id}, update={'$inc': {'views': 1}})
    return ""


@images_bp.route('/images/count/', methods=['GET'])
def get_images_count():
    return jsonify({"count": images_collection.count_documents({})})


def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in ALLOWED_EXTENSIONS


@images_bp.route('/images/upload/', methods=['POST'])
@cross_origin()
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
        print(os.path.join(UPLOAD_FOLDER, filename))
        el.save(os.path.join(UPLOAD_FOLDER, filename))
        data = handleImage(filename, exifs)
        images_collection.insert_one(data)
    return Response(status=200, mimetype='application/json')


@images_bp.route('/disk/', methods=['GET'])
@cross_origin()
def get_disk():
    total, used, free = shutil.disk_usage("/")
    total = round(total / (2**30), 1)
    used = round(used / (2**30), 1)
    free = round(free / (2**30), 1)
    percentage = round(used / total * 100, 1)
    return jsonify({"total": f'{total}GB', "used": f'{used}GB', "free": f'{free}GB', 'percentage': percentage})


@images_bp.route('/browserstats/', methods=['GET'])
@cross_origin()
def get_browser_stats():
    output = []
    B = browsers_collection.find()
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


@images_bp.route('/images/allviews', methods=['GET'])
@cross_origin()
def get_all_views():
    output = []
    for image in images_collection.find():
        output.append(
            {"download": image["download"], "view": image["view"], "image": image["image"]})
    return jsonify(output)


@images_bp.route('/images/test', methods=['GET'])
@cross_origin()
def create_image_test():
    images_collection.insert_one({"image": {"id": "1", "compressed": "https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg",
                                            "original": "https://cdn.pixabay.com/photo/2023/03/18/16/26/ha-giang-7860907_640.jpg", "author": "hamza", "exif": "girl, flowers, asian", "downloads": "1", "hasFace": True}, "download": "1", "view": "1"})
    return jsonify({'message': 'image created'})
