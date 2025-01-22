import tensorflow as tf
import numpy as np
import os
import json
from django.apps import apps
from django.conf import settings
from django.http import JsonResponse

def preprocess_image_function(image_path, target_size):
  image = tf.io.read_file(image_path)
  image = tf.image.decode_image(image, channels=3)

  image_resized = tf.image.resize(image, target_size)
  image_normalized = image_resized / 255.0

  preprocessed_image = np.expand_dims(image_normalized, axis=0)

  return preprocessed_image

def predict_one_image(preprocessed_image):
    model = apps.get_app_config('DiseaseDetection').disease_detection_model
    print("Prediction of disease in leaf done")

    predictions = model.predict(preprocessed_image)
    return predictions

def get_classes():
    # Finding different labels of class
    with open(os.path.join(settings.BASE_DIR, 'savedModels', 'class_indices.json'), "r") as f:
        class_indices = json.load(f)

    # Invert the dictionary to map labels to class names
    class_labels = {v: k for k, v in class_indices.items()}
    return class_labels

def check_disease_api(request):
    file_path = request.session.get('file_path', None)
    
    if not file_path:
        return JsonResponse({'error': 'No file path found'})

    preprocessed_image = preprocess_image_function(file_path, target_size=(224, 224))
    result = predict_one_image(preprocessed_image)
    print("Hello1")

    print("Result: ", result)

    result_as_list = result[0].tolist()

    class_labels = get_classes()

    final_result = {class_labels[i]: f"{result_as_list[i] * 100:.2f}%" for i in range(len(result_as_list))}

    print(f"Final Result: \n", final_result)
    print(file_path)

    # Check if the file exists before trying to delete it
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the file
        print(f"{file_path} has been deleted successfully.")
    else:
        print(f"{file_path} file does not exist.")

    # JSON response in here
    return JsonResponse(final_result)