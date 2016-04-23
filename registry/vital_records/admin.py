from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (RegistryUser, Person, Registrar, Residence, ApplicantInfo,
                     BirthNote, BirthEvidence, BirthNoteLaw, BirthPlace)

admin.site.register(RegistryUser, UserAdmin)

admin.site.register(Person)
admin.site.register(ApplicantInfo)
admin.site.register(Residence)
admin.site.register(Registrar)
admin.site.register(BirthNote)
admin.site.register(BirthPlace)
admin.site.register(BirthEvidence)
admin.site.register(BirthNoteLaw)
