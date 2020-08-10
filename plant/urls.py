from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import PlantUpdateView


urlpatterns = [
    path('', views.all_plants, name='all_plants'),
    path('<plant_id>/plant_detail/', views.plant_detail, name='plant_detail'),
    path('<plant_id>/nursery_plant_detail/', views.nursery_plant_detail, name='nursery_plant_detail'),
    path('<int:pk>/update/', PlantUpdateView.as_view(), name="plant_update"),
    path('add_favorite/', views.add_favorite, name='favorite'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('new/', views.sow_plant, name="plant_create"),
]
