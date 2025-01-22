from django.conf import settings
from django.http import JsonResponse
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def api_key_required(view_func):
    def wrapper(request, *args, **kwargs):
        api_key = request.headers.get("DETECTION-API-KEY")
        if int(api_key) == int(os.getenv("DETECTION-API-KEY")):
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Invalid API key'}, status=401)
    return wrapper
