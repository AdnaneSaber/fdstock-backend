import os
import json
from PIL import Image
import piexif
from mining import get_tags
import face_recognition
from datetime import datetime

# set the directory containing the images
image_dir = "images"
original_dir = "imagesapi/"
# set the directory to save the thumbnails
thumb_dir = "imagesapi/thumbnails"

# set the directory to save the compressed images
comp_dir = "imagesapi/compressed"

# set the maximum size for the thumbnails and compressed images
max_size = (128, 128)

# initialize an empty list to hold the image data
image_data = []

# loop through all the files in the directory
for file_name in os.listdir(image_dir):
    if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
        # initialize a dictionary to hold the data for this image
        image_dict = {"downloads": 0, "views": 0}

        # get the full path to the file
        file_path = os.path.join(image_dir, file_name)

        # open the image file
        with Image.open(file_path) as img:
            # get the image dimensions
            width, height = img.size

            # determine whether the image is portrait, landscape, or square
            if width > height:
                image_dict["size"] = "landscape"
            elif width < height:
                image_dict["size"] = "portrait"
            else:
                image_dict["size"] = "square"
            # extract id from file_path knowing that filepath is like this: AdobeStock_583093600_Preview.jpeg and the id is the number before the underscore
            id = file_name.split("_")[1]
            name = file_name.split('.')[0]
            image_dict["exif"] = get_tags(id)

            # use face_recognition library to detect faces in the image
            im = face_recognition.load_image_file(file_path)
            face_locations = face_recognition.face_locations(im, model="cnn")
            if len(face_locations) > 0:
                image_dict["hasFace"] = True
            else:
                image_dict["hasFace"] = False

            # create a thumbnail of the image
            thumb_path = os.path.join(thumb_dir, file_name)
            img.thumbnail(max_size)
            img.save(thumb_path)

            # create a compressed version of the image
            comp_path = os.path.join(comp_dir, file_name)
            img.save(comp_path, optimize=True, quality=85)

            # Get the current date and time
            current_datetime = datetime.utcnow()

            # Format the date in ISO 8601 format
            date_creation = current_datetime.isoformat()
            # add other image metadata to the dictionary
            image_dict["id"] = id
            image_dict["compressed"] = comp_path
            image_dict["thumbnail"] = thumb_path
            image_dict["original"] = os.path.join(original_dir, file_name)
            image_dict["name"] = name
            image_dict["date_creation"] = date_creation

            # add the image dictionary to the list of image data
            image_data.append(image_dict)
            print(image_dict)
# create a JSON object containing the image data
json_data = {"images": image_data}

# output the JSON data to a file
with open("output.json", "w") as json_file:
    json.dump(json_data, json_file)
