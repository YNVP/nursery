from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(PreviousOrders)
admin.site.register(UserOrders)
admin.site.register(Order)
admin.site.register(OrderPlant)
admin.site.register(CurrentOrder)
admin.site.register(OnDeliveryOrders)
