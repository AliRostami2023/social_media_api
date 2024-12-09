from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'username', 'is_active', 'is_admin']

admin.site.register(ProfileUser)
