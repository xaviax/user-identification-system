from django.db import models
from accounts.models import User
from rooms.models import System
# Create your models here.



class UserSystemMap(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='system_mappings')

    system=models.ForeignKey(System,on_delete=models.CASCADE, related_name='user_mappings')
    system_user_id=models.CharField(max_length=50,unique=True)

    class Meta:
        unique_together = ('user','system')

    def __str__(self):
        return f"User :{self.user.username} -> System: {self.system.name} ({self.system_user_id}) "


