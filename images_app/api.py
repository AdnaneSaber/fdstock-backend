import os
from PIL import Image
import face_recognition
import shutil
import random
from datetime import datetime
import torch
from torchvision import models, transforms
def predict_image_name(image_path):
    # Load the pre-trained ResNet50 model
    model = models.resnet50(pretrained=True)
    model.eval()

    # Load and preprocess the image
    image = Image.open(image_path)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    # If you have a GPU, use it for faster inference
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_batch = input_batch.to(device)
    model = model.to(device)

    # Perform the forward pass
    with torch.no_grad():
        output = model(input_batch)

    # Load the ImageNet class labels
    with open("imagenet_classes.txt") as f:
        labels = f.readlines()
    labels = [label.strip() for label in labels]

    # Get the predicted class label
    _, predicted_idx = torch.max(output, 1)
    predicted_label = labels[predicted_idx.item()]
    return predicted_label
# loop through all the files in the directory
def handleImage(file_name: str, exifs: str):
    # set the directory containing the images
    image_dir = "uploads"
    original_dir = "images/"
    # set the directory to save the thumbnails
    thumb_dir = "images/thumbnails"

    # set the directory to save the compressed images
    comp_dir = "images/compressed"

    # set the maximum size for the thumbnails and compressed images
    max_size = (300, 300)
    min_num = 100000000  # Minimum 9-digit number
    max_num = 999999999    
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
            random_number = random.randint(min_num, max_num)
            id = str(random_number)
            name = file_name.split('.')[0]
            image_dict["exif"] = exifs

            # use face_recognition library to detect faces in the image
            im = face_recognition.load_image_file(file_path)
            face_locations = face_recognition.face_locations(im)
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
            or_dir = os.path.join(original_dir, file_name)
            shutil.move(file_path, or_dir)
            # Get the current date and time
            current_datetime = datetime.utcnow()

            # Format the date in ISO 8601 format
            date_creation = current_datetime.isoformat()
            # add other image metadata to the dictionary
            image_dict["id"] = id
            image_dict["compressed"] = os.path.join("imagesapi/compressed", file_name)
            image_dict["thumbnail"] = os.path.join("imagesapi/thumbnails", file_name)
            image_dict["original"] = os.path.join("imagesapi/", file_name)
            image_dict["name"] = name
            image_dict["date_creation"] = date_creation
            return image_dict

