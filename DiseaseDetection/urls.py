from django.urls import path
from . import views

urlpatterns = [
    path('check_disease_api', views.check_disease_api, name="check_disease_api"),
]