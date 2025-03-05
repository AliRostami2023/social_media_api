from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'username', 'email', 'is_active', 'is_admin']
    list_filter = ['is_admin', 'is_active']
    search_fields = ['username', 'email']
    list_per_page = 100
    

@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'avatar', 'gender']
    list_filter = ['gender']
    search_fields = ['full_name']
    list_per_page = 100


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'created', 'expired_date']
    list_per_page = 100


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created', 'is_used']
    list_filter = ['is_used']
    list_per_page = 100
    