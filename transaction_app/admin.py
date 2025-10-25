from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
    ('Additional info', {'fields': ('city', 'country','area')}),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password') and not obj.password.startswith("pbkdf2_"):
            obj.set_password(form.cleaned_data.get('password'))

        super().save_model(request, obj, form, change)



admin.site.register(Area)
admin.site.register(Room)
admin.site.register(System)
admin.site.register(UserSystemMap)


