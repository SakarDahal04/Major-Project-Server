import os

from django.core.wsgi import get_wsgi_application

settings_module = "MajorProject.deployment" if "WEBSITE_HOST" in os.environ else "MajorProject.settings"
# WEBSITE_HOSTNAME is provided by azure

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MajorProject.settings")

application = get_wsgi_application()
