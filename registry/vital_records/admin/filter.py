from django.contrib.admin import BooleanFieldListFilter
from django.utils.translation import ugettext as _


class BaseBooleanFieldListFilter(BooleanFieldListFilter):
    choice_map = (
        (None, _('All')),
        ('1', _('Yes')),
        ('0', _('No'))
    )

    def choices(self, cl):
        for lookup, title in self.choice_map:
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


class GenderFieldListFilter(BaseBooleanFieldListFilter):
    choice_map = (
        (None, _('Any')),
        ('0', _('Female')),
        ('1', _('Male'))
    )

