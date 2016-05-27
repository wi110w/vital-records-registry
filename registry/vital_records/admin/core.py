from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ..forms import PersonAdminForm
from ..models import RegistryUser, Person, Registrar, Residence, ApplicantInfo

admin.site.register(RegistryUser, UserAdmin)

admin.site.register(Residence)
admin.site.register(Registrar)


@admin.register(ApplicantInfo)
class ApplicantInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonAdminForm
    list_display = ('first_name', 'last_name', 'patronymic')
