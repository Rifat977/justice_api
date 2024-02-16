from django.contrib import admin
from . import models

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'user_type', 'email_verified']
    search_fields = ['username', 'email']

admin.site.register(models.CustomUser, CustomUserAdmin)

admin.site.register(models.EmailVerificationOTP)
