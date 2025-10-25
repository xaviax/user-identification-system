from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

#This is the Django User Model which contains further fields based on requirements


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


class Room(models.Model):
    name=models.CharField(max_length=100)
    area=models.ForeignKey(Area,on_delete=models.CASCADE,related_name='rooms')

    def __str__(self):
        return f"Room: {self.name} -> Area: {self.area}"



class System(models.Model):
    name=models.CharField(max_length=100)
    room=models.ForeignKey(Room,on_delete=models.CASCADE,related_name='systems')

    def __str__(self):
        return f"System: {self.name} -> Room: {self.room}"


class UserSystemMap(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='system_mappings')

    system=models.ForeignKey(System,on_delete=models.CASCADE, related_name='user_mappings')
    system_user_id=models.CharField(max_length=50,unique=True)

    class Meta:
        unique_together = ('user','system')

    def __str__(self):
        return f"User :{self.user.username} -> System: {self.system.name} ({self.system_user_id}) "


