from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from plant.models import Plant
from nursery.models import Nursery
from django.urls import reverse
from django.db.models.signals import pre_save
from users.models import Address


class OrderPlant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    packed = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.plant.name}"

    def get_total_plant_price(self):
        self.nursery_name = self.plant.nursery.name
        return self.quantity * self.plant.price

    def get_final_price(self):
        return self.get_total_plant_price()

    def get_absolute_url(self):
        return reverse("plant_order_detail", args=[str(self.id)])


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plants = models.ManyToManyField(OrderPlant)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_plant in self.plants.all():
            total += order_plant.get_final_price()
        return total


class OnDeliveryOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username


class PreviousOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_plant in self.plants.all():
            total += order_plant.get_final_price()
        return total

    def get_absolute_url(self):
        return reverse("landing_page")


class UserOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(PreviousOrders)

    def get_absolute_url(self):
        return reverse("user_order_detail", args=[str(self.id)])


class CurrentOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plants = models.ManyToManyField(OrderPlant)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_plant in self.plants.all():
            total += order_plant.get_final_price()
        return total
