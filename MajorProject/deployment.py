import os
from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.environ(['SECRET'])

# ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]    # This will be the azure url which will only serve the code in this project
ALLOWED_HOSTS = ['*']    # This will be the azure url which will only serve the code in this project

CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]

DEBUG = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATICFILES_STORAGE = "CONNECT USING WHITENOISE"
# STATIC_ROUTE = "STORAGE FOLDER PATH"
# DATABASE

