from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RegistryUser
admin.site.register(RegistryUser, UserAdmin)
