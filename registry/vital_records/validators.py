from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def non_zero_integer(msg):
    def check(value):
        if value == 0:
            raise ValidationError(msg)
    return check

def birth_date_not_future(value):
    if value >= timezone.now().date():
        raise ValidationError(_('Birth date cannot be future'))
