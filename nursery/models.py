from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import pre_save
from users.utils import unique_slug_generator, random_string_generator
from django.urls import reverse


class Nursery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(default='plant.jpeg', upload_to='plant_pics')
    slug = models.SlugField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("nursery_detail", args=[str(self.name)])

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance, random_string_generator())


pre_save.connect(pre_save_receiver, sender=Nursery)
