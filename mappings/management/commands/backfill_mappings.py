from django.core.management.base import BaseCommand

from accounts.models import User
from rooms.models import System
from mappings.services import create_mappings_for_user,create_mappings_for_system

class Command(BaseCommand):
    help = "Backfill UserSystemMap for existing users and systems"


    def handle(self, *args, **options):

            self.stdout.write("Backfilling  for users...")
            for user in User.objects.filter(area__isnull=False):
                create_mappings_for_user(user)

            self.stdout.write("Backfilling mappings for systems...")
            for system in System.objects.all():
                create_mappings_for_system(system)
            self.stdout.write(self.style.SUCCESS("Backfilling mappings for users..."))
