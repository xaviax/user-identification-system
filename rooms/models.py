from django.db import models
from accounts.models import Area

# Create your models here.

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