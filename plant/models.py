from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from nursery.models import Nursery
from django.urls import reverse


class Plant(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(default='plant.jpeg', upload_to='plant_pics')
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    favorite = models.ManyToManyField(User, related_name="favorite")
    nursery = models.ForeignKey(Nursery, on_delete=models.CASCADE)
    stock = models.IntegerField()
    published_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plant_detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        img.save(self.image.path)
