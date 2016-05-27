from django.contrib import admin
from django.contrib.admin import BooleanFieldListFilter, DateFieldListFilter
from django.utils.translation import ugettext as _

from ..forms import BirthNoteAdminForm
from ..models import BirthNote, BirthEvidence, BirthNoteLaw, BirthPlace

admin.site.register(BirthPlace)
admin.site.register(BirthEvidence)
admin.site.register(BirthNoteLaw)


class GenderFieldListFilter(BooleanFieldListFilter):
    def choices(self, cl):
        for lookup, title in (
                (None, _('Any')),
                ('0', _('Female')),
                ('1', _('Male'))):
            yield {
                'selected': self.lookup_val == lookup and not self.lookup_val2,
                'query_string': cl.get_query_string({
                    self.lookup_kwarg: lookup,
                }, [self.lookup_kwarg2]),
                'display': title,
            }
        from django.db import models
        if isinstance(self.field, models.NullBooleanField):
            yield {
                'selected': self.lookup_val2 == 'True',
                'query_string': cl.get_query_string({
                    self.lookup_kwarg2: 'True',
                }, [self.lookup_kwarg]),
                'display': _('Unknown'),
            }


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
    list_display = (
        'note_number', 'compose_date', 'child_name', 'child_last_name', 'child_patronymic',
        'children_born_count', 'child_number'
    )
    date_hierarchy = 'compose_date'
    list_filter = (
        ('child_gender', GenderFieldListFilter),
        'children_born_count', 'created_by',
        ('birth_date', DateFieldListFilter),
        'language'
    )
    filter_horizontal = ['birth_evidences', 'parents']
    search_fields = (
        'note_number', 'child_name', 'child_last_name', 'child_patronymic'
    )

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
