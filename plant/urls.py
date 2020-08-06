from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('plant_detail/<int:plant_id>', views.plant_detail, name='plant_detail'),
]
