from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import BirthNoteAdminForm, PersonAdminForm
from .models import (RegistryUser, Person, Registrar, Residence, ApplicantInfo,
                     BirthNote, BirthEvidence, BirthNoteLaw, BirthPlace)

admin.site.register(RegistryUser, UserAdmin)

admin.site.register(Residence)
admin.site.register(Registrar)
admin.site.register(BirthPlace)
admin.site.register(BirthEvidence)
admin.site.register(BirthNoteLaw)


class BirthNoteAdmin(admin.ModelAdmin):
    form = BirthNoteAdminForm
    fieldsets = [
        ('Common note info', {
            'fields': (
                'note_number',
                'compose_date',
                ('was_restored', 'was_revoked'),
                'language',
                'official_info',
                'created_by',
                'notes',
                'registrar'
            )
        }),
        ('Child info', {
            'fields': (
                'birth_date',
                'birth_place',
                'child_name',
                'child_last_name',
                'child_patronymic',
                'child_gender',
                'child_number',
                'stillborn'
            )
        }),
        ('Birth note details', {
            'fields': (
                'law',
                'deadline_passed',
                'children_born_count',
                'birth_evidences',
                'applicant'
            )
        }),
        ('Parents info', {
            'fields': (
                'parents',
                'father_info_reason',
                'military_service'
            )
        })
    ]
    readonly_fields = ['created_by']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(BirthNote, BirthNoteAdmin)

class ApplicantInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'patronymic')

admin.site.register(ApplicantInfo, ApplicantInfoAdmin)

class PersonAdmin(admin.ModelAdmin):
    form = PersonAdminForm
    list_display = ('first_name', 'last_name', 'patronymic')

admin.site.register(Person, PersonAdmin)
