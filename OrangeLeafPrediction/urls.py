from django.urls import path
from . import views

urlpatterns = [
    path('api/check-leaf', views.check_leaf_api, name='check_leaf_api'),
]
