from django.contrib import admin

from ..forms import BirthNoteAdminForm
from ..models import BirthNote, BirthEvidence, BirthNoteLaw, BirthPlace

admin.site.register(BirthPlace)
admin.site.register(BirthEvidence)
admin.site.register(BirthNoteLaw)


@admin.register(BirthNote)
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
                'father_info_reason'
            )
        })
    ]
    readonly_fields = ['created_by']
    list_display = ('note_number', 'compose_date')

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)