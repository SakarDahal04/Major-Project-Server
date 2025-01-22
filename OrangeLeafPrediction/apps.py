# myapp/apps.py
from django.apps import AppConfig
import pickle
from django.conf import settings
from tensorflow.keras.applications import ResNet50
import os

class OrangeLeafPrediction(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OrangeLeafPrediction'

    # Global variable to store the model
    leaf_detection_model = None
    feature_extractor = None

    def ready(self):
        global loaded_model
        # Path to your model file
        leaf_detection_model_path = os.path.join(settings.BASE_DIR, 'savedModels', 'ocsvm_model.pkl')
        with open(leaf_detection_model_path, 'rb') as file:
            self.leaf_detection_model = pickle.load(file)
        print("Orange Detection Model loaded successfully!")

        self.feature_extractor = ResNet50(weights="imagenet", include_top=False, pooling="avg")
        print("ResNet50 loaded for feature extraction")

