from django.contrib import admin
from user.models import *
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
            'user_name',
            'phone',
            'address',
            'city',
            'country'
        )