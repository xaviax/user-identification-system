from django.db import transaction
from accounts.models import User
from rooms.models import System
from .models import UserSystemMap
import  uuid

def _generate_system_user_id():
    """This generates a short, unique-ID for user-system mapping"""
    return uuid.uuid4().hex[:10]


'''
After the user is saved, the admin code calls the mapping service 

create_mappings_for_user(obj) 

-create_mappings_for_user(user)
    --  if user.area is None, then immediately return 
    -- then, query all system objects whose room__area ==user.area
    --then, compute which of those systems already have a UserSystemMap for this user
    --create UserSystemMap objects in memory for missing systems
    -- insert all mappings in one call 
    -- this whole function is wrapped with @transaction.atomic so if something fails, no partial changes remain 

'''


@transaction.atomic
def create_mappings_for_user(user):
    """
    So, when a user is created, automatically create mappings
    for all systems in the same area

    -This only runs if a user is assigned an area
    -Won't create duplicate mappings
    """

    if not user.area:
        return []

    systems = System.objects.filter(room__area=user.area)

    if not systems.exists():
        return []


    existing_system_ids = set(
        UserSystemMap.objects.filter(user=user,system__in=systems).values_list("system_id",flat=True)

    )


    new_mappings = [
        UserSystemMap(
            user=user,
            system=system,
            system_user_id=_generate_system_user_id(),
        )

        for system in systems
        if system.id not in existing_system_ids
    ]

    if new_mappings:
        UserSystemMap.objects.bulk_create(new_mappings)

    return new_mappings



@transaction.atomic
def create_mappings_for_system(system):
    """
        When a system is created, automatically create mappings
        all users that belong in that area will be assigned the system
    """


    area = system.room.area

    users = User.objects.filter(area=area)
    if not users.exists():
        return []

    #Prevent Duplicate mappings
    existing_user_ids = set(
        UserSystemMap.objects.filter(
            system=system,
            user__in=users,
        ).values_list("user_id",flat=True)


    )

    new_mappings = [
        UserSystemMap(
            user=user,
            system=system,
            system_user_id=_generate_system_user_id(),
        )

        for user in users
        if user.id not in existing_user_ids
    ]
    if new_mappings:
        UserSystemMap.objects.bulk_create(new_mappings)

    return new_mappings




