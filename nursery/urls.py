from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.contrib import messages


urlpatterns = [
    path('', views.manager_home, name='manager_home'),
    path('<slug:slug>/nursery_update/',
         views.NurseryUpdateView.as_view(), name='nursery_update'),
    path('register/', views.register, name='nursery_register'),
    path('nursery_orders/', views.nursery_orders, name='nursery_orders'),
    path('nursery_detail/<str:name>', views.nursery_detail, name='nursery_detail'),
    path('add_pack_status/', views.add_pack_status, name='add_pack_status'),
    path('add_delivery_status/', views.add_delivery_status,
         name='add_delivery_status'),
    path('add_receive_status/', views.add_receive_status,
         name='add_receive_status'),
]
