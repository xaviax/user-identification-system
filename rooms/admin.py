from django.contrib import admin
from .models import Room, System
from django import forms
from accounts.models import Area
from mappings.services import create_mappings_for_system
from mappings.models import UserSystemMap
# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name','area')



@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ('name','room','area_display')
    readonly_fields = ('area_display')
    fields = ('name','room','area_display')

    def area_display(self, obj):
        return obj.room.area.name if obj and obj.room and obj.room.area else '-'

    area_display.short_description = 'Area'

    def save_model(self, request, obj, form, change):
        created = not change
        area_changed=False
        old_area=None

        if change:
            old_system = System.objects.get(pk=obj.pk)
            old_area = old_system.room.area if old_system.room else None
            new_area = obj.room.area if obj.room else None
            if old_area != new_area:
                area_changed =True

        super().save_model(request, obj, form, change)

        if created or area_changed:
            if old_area and old_area !=(obj.room.area if obj.room else None):
                UserSystemMap.objects.filter(system=obj).delete()
        create_mappings_for_system(obj)

    def delete_model(self, request, obj):
        UserSystemMap.objects.filter(system=obj).delete()
        super().delete_model(request, obj)