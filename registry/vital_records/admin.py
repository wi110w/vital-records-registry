from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (RegistryUser, Person, Registrar, Residence, ApplicantInfo,
                     BirthNote, BirthEvidence, BirthNoteLaw, BirthPlace)
from .models import (DeathNote, DeathPlace, DeathEvidence)


class DeathNoteAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Відомості щодо актового запису про смерть',   {'fields': ['language', 'compose_date', 'status',
                                                                    'rehabilitation_statements', 'registrar',
                                                                    'official_info', 'notes']}),
        ('Відомості про померлу особу',     {'fields': ['person', 'date_of_death', 'death_place', 'death_reason',
                                                        'death_evidence']}),
        ('Відомості про заявника',      {'fields': ['applicant']}),
        ('Відомості про вилучені документи у зв\'язку з державною реєстрацією смерті особи',      {'fields': [
            'discarded_documents'
        ]}),
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
