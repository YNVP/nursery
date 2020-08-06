from django.db import models
from django.contrib.auth.models import User
from PIL import Image



class Plant(models.Model, HitCountMixin):
    name = models.CharField(max_length=200)
    image = models.ImageField(default='plant.jpeg', upload_to='plant_pics')
    description = tinymce_models.HTMLField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    favorite = models.ManyToManyField(User, related_name="favorite")
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