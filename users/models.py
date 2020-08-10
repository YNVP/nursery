from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from plant.models import Plant
from nursery.models import Nursery
from django.urls import reverse
from django.db.models.signals import pre_save
from .utils import unique_slug_generator, random_string_generator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='user.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

    def get_absolute_url(self):
        return reverse("profile")


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance, random_string_generator())


pre_save.connect(pre_save_receiver, sender=Address)
