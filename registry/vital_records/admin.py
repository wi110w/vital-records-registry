from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from .models import (RegistryUser, Person, Registrar, Residence, ApplicantInfo,
                     BirthNote, BirthEvidence, BirthNoteLaw, BirthPlace)
from .models import (DeathNote, DeathPlace, DeathEvidence)


class DeathNoteAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Note info'), {'fields': ['note_number', 'language', 'compose_date', 'status','rehabilitation_statements',
                                     'registrar', 'official_info', 'notes']}),
        (_('Death person info'), {'fields': ['person', 'date_of_death', 'death_place', 'death_reason',
                                             'death_evidence']}),
        (_('Applicant info'), {'fields': ['applicant']}),
        (_('Discarded documents info'), {'fields': ['discarded_documents']}),
    ]


admin.site.register(RegistryUser, UserAdmin)

admin.site.register(Person)
admin.site.register(ApplicantInfo)
admin.site.register(Residence)
admin.site.register(Registrar)
admin.site.register(BirthNote)
admin.site.register(BirthPlace)
admin.site.register(BirthEvidence)
admin.site.register(BirthNoteLaw)
admin.site.register(DeathNote, DeathNoteAdmin)
admin.site.register(DeathPlace)
admin.site.register(DeathEvidence)
