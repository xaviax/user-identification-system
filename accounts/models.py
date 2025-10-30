from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Area(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name



class User(AbstractUser):

    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    area=models.ForeignKey(Area,on_delete=models.CASCADE,related_name='users',blank=True, null=True)

    def __str__(self):
        return f"User: {self.username} -> Area: {self.area}"
