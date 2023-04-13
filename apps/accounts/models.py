import os
import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from .utils import ResizingImages
# Create your models here.


def upload_thumbnail(instance, filename):
    base, extension = filename.rsplit(".", 1)
    # Ruta completa de la imagen anterior
    today = datetime.date.today()
    thumbnail_path = f'accounts/{instance.username}/{today.year}/{today.month}/{today.day}/{instance.username}.{extension}'
    full_path = os.path.join(settings.MEDIA_ROOT, thumbnail_path)

    if os.path.exists(full_path):
        os.remove(full_path)

    return thumbnail_path


class CustomUser(AbstractUser):
    class Genders(models.TextChoices):
        NO_BINARY = 'NB', 'No Binario'
        FEMALE = 'F', 'Femenino'
        MALE = 'M', 'Masculino'

    thumbnail = models.ImageField(upload_to=upload_thumbnail, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    karma = models.PositiveIntegerField(default=0)
    display_name = models.CharField(max_length=50, blank=True)
    about = models.TextField(blank=True)
    gender = models.CharField(choices=Genders.choices,
                              default=Genders.NO_BINARY,
                              max_length=2)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk and not self.display_name:
            self.display_name = self.username
        super().save(*args, **kwargs)
        if self.thumbnail:
            image_resizing = ResizingImages
            image_resizing.resize_image_square(self.thumbnail.path)

    @property
    def get_display_name(self):
        if self.display_name:
            return f'Profile of {self.display_name}'
        else:
            return f'Profile of {self.username}'

    @property
    def get_display_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        return f'{settings.STATIC_URL}img/default-thumbnail.jpg'
    
