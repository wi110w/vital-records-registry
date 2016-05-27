from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.contrib.auth.admin import UserAdmin

from .filter import GenderFieldListFilter, MarriageStatusFieldListFilter
from ..forms import PersonAdminForm
from ..models import RegistryUser, Person, Registrar, Residence, ApplicantInfo

admin.site.register(RegistryUser, UserAdmin)

admin.site.register(Residence)
admin.site.register(Registrar)


@admin.register(ApplicantInfo)
class ApplicantInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic', 'residence')
    search_fields = (
        'first_name', 'last_name', 'patronymic'
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonAdminForm
    list_display = (
        'first_name', 'last_name', 'patronymic', 'date_of_birth',
        'gender', 'family_status', 'residence'
    )
    list_display_links = ('first_name', 'last_name', 'patronymic')
    date_hierarchy = 'date_of_birth'
    list_filter = (
        ('gender', GenderFieldListFilter),
        ('family_status', MarriageStatusFieldListFilter),
        ('date_of_birth', DateFieldListFilter)
    )
    search_fields = (
        'first_name', 'last_name', 'patronymic'
    )
