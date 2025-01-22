from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.apps import apps

from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .middleware import api_key_required

import numpy as np
import os
import tensorflow as tf
from joblib import load
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.resnet50 import preprocess_input

# Function to ask for the image from the user
def get_image_path_from_user(request, form):
    if form.is_valid():
        file = request.FILES['image']

        file_path = os.path.join(settings.BASE_DIR, 'uploads', file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file_path
    else:
        return JsonResponse({"Error": "Form is not valid"})

# Function to preprocess the image


def preprocess_image(image_path, target_size):
    image = tf.io.read_file(image_path)
    image = tf.image.decode_image(image, channels=3)

    image_resized = tf.image.resize(image, target_size)
    image_normalized = image_resized / 255.0

    preprocessed_image = np.expand_dims(image_normalized, axis=0)

    return preprocessed_image

# Function to load the model
def orange_leaf_prediction_load_model():
    model = apps.get_app_config('OrangeLeafPrediction').leaf_detection_model
    return model

# Function for the prediction of the image
def predict_if_orange_image(features):
    model = orange_leaf_prediction_load_model()

    result = model.predict(features)
    print("Prediction of Disesase of Orange Leaf Done")
    score = model.decision_function(features)
    return result, score


def extract_features(image_path):
    # Load the pre-trained ResNet50 model
    feature_extractor = apps.get_app_config('OrangeLeafPrediction').feature_extractor
    print("Feature extracted using ResNet50")

    """Extract features from an image using ResNet50."""
    image = load_img(image_path, target_size=(224, 224))  # Resize to 224x224
    image = img_to_array(image)  # Convert to array
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = preprocess_input(image)  # Pre-process for ResNet50
    features = feature_extractor.predict(image)  # Extract features
    return features.flatten()  # Flatten the features

@api_view(['POST'])
@api_key_required
def check_leaf_api(request):
    if 'image' not in request.FILES:
        return Response({"error": "No image provided"}, status=400)

    # Save the uploaded image
    image = request.FILES['image']
    file_path = os.path.join(settings.BASE_DIR, 'uploads', image.name)
    with open(file_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    # Extract features and predict
    features = extract_features(file_path)
    result, score = predict_if_orange_image([features])

    # Prepare response
    if result[0] == 1:
        request.session['file_path'] = file_path
        return redirect("check_disease_api")  # Redirect to another URL path

    else:
        response = {
            "message": "The image is NOT an Orange Leaf.",
            "score": round(score[0], 2),
            "status": "failure",
        }

    print(response)

    # Check if the file exists before trying to delete it
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the file
        print(f"{file_path} has been deleted successfully.")
    else:
        print(f"{file_path} does not exist.")

    return Response(response)
