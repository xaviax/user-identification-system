from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
import uuid


def generate_system_user_uuid():
    return uuid.uuid4().hex[:10]

@receiver(post_save, sender=User)
def create_user_system_maps(sender, instance, created, **kwargs):
    #Now if a new user is created and assigned an area, then
    # that user must have access to all the systems in that area
    #therefore when a new user is created, this is auto run
    if created and instance.area:

        systems = System.objects.filter(room__area=instance.area)

        for system in systems:
            UserSystemMap.objects.create(
                user=instance,
                system=system,
                system_user_id=generate_system_user_uuid()
            )


@receiver(post_save, sender=System)
#If a new system is added to a room in an area, then all the users assigned to that room would have access to that new system
def create_system_user_map(sender, instance, created, **kwargs):
    if created :
        area=instance.room.area
        users=User.objects.filter(area=area)

        for user in users:
            UserSystemMap.objects.create(
                user=user,
                system=instance,
                system_user_id=generate_system_user_uuid()
            )



