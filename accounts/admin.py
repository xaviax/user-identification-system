from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from mappings.models import UserSystemMap
from .models import Area, User

# Register your models here.

'''
This is part of the alt for signals, 
Now when a user is created through the django admin panel, 
then django calls super().save_model(...) which performs the following:

- Detects whether the created user is a new object 
  -- created = not change 
  
- Ensures that the password is properly hashed 
    -- obj.set_password()
    
- Lastly, calls the super().save_model(...) which writes the user row in DB


      
'''

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {'fields':('city','country','area')}),
    )

    def save_model(self,request,obj,form,change):
        #detects if the user is created
        created = not change
        area_changed = False
        old_area = None

        if change:
            old_user =User.objects.get(pk=obj.pk)
            old_area = old_user.area
            if old_area != obj.area:
                area_changed = True

        #this below insures password hashing
        if form.cleaned_data.get('password') and not obj.password.startswith("pbkdf2_"):
            obj.set_password(form.cleaned_data.get('password'))

        super().save_model(request,obj,form,change)

        from mappings.services import create_mappings_for_user
        from mappings.models import UserSystemMap

        if created or  area_changed:
            if old_area and old_area != obj.area:
                UserSystemMap.objects.filter(user=obj).delete()

        if obj.area:
            create_mappings_for_user(obj)






@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',)



