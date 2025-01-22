# myapp/apps.py
from django.apps import AppConfig
import pickle
from django.conf import settings
import os

class DiseaseTypePrediction(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DiseaseDetection'

    # Global variable to store the model
    disease_detection_model = None

    def ready(self):
        global disease_detection_model
        # Path to your model file
        disease_detection_model_path = os.path.join(settings.BASE_DIR, 'savedModels', 'model_pkl_with_conv.pkl')
        with open(disease_detection_model_path, 'rb') as file:
            self.disease_detection_model = pickle.load(file)
        print("Disease Detection Model loaded successfully!")
