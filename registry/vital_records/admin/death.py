from django.contrib import admin
from django.utils.translation import ugettext as _

from ..models import DeathNote, DeathPlace, DeathEvidence


@admin.register(DeathNote)
class DeathNoteAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Note info'), {
            'fields': (
                'note_number',
                'language',
                'compose_date',
                'status',
                'rehabilitation_statements',
                'registrar',
                'official_info',
                'notes'
            )
        }),
        (_('Death person info'), {
            'fields': (
                'person',
                'date_of_death',
                'death_place',
                'death_reason',
                'death_evidence'
            )
        }),
        (_('Applicant info'), {'fields': ['applicant']}),
        (_('Discarded documents info'), {'fields': ['discarded_documents']}),
    ]

admin.site.register(DeathPlace)
admin.site.register(DeathEvidence)
