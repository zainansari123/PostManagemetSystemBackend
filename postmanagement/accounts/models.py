from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    profile_img = models.ImageField(upload_to='profile_images', null=True)
    country_code = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    address = models.CharField(max_length=40,blank=True)
    gender=models.CharField(max_length=10, blank=True)
    def __str__(self):
        return self.username