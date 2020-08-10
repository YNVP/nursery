from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views as order_views
from django.db.models.signals import pre_save


urlpatterns = [
    path('add_to_cart/', order_views.add_to_cart, name='add_to_cart'),
    path('orders/', order_views.orders, name='user_orders'),
    path('checkout/', order_views.checkout, name='checkout'),
    path('confirm_checkout/', order_views.confirm_checkout,
         name='confirm_checkout'),
    path('delete_item/', order_views.delete_item, name='item_delete'),
    path('delete_order/', order_views.delete_order, name='order_delete'),
    path('save_order/', order_views.save_order, name='order_save'),
    path('<order_id>/plant_order_detail/',
         order_views.plant_order_detail, name='plant_order_detail'),
    path('on_delivery/', order_views.on_delivery, name='on_delivery'),
    path('previous_orders/', order_views.previous_orders, name='previous_orders'),
]
