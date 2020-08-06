from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from plant.models import Plant


class Nursery(models.Model, HitCountMixin):
    name = models.CharField(max_length=200)
    image = models.ImageField(default='plant.jpeg', upload_to='plant_pics')
    plants = models.ManyToManyField(Plant, related_name='nursery_plants')
    published_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)