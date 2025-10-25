from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Area)
admin.site.register(Room)
admin.site.register(System)
admin.site.register(UserSystemMap)


