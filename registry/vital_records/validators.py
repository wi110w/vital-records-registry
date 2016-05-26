from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext as _


@deconstructible
class BaseCallableValidator(object):
    compare = lambda self, a, b: a is not b
    message = _('Ensure this value is %(limit_value)s (it is %(show_value)s).')
    code = 'limit_value'

    def __init__(self, limit_callable, message=None):
        self.limit_callable = limit_callable
        if message:
            self.message = message

    def __call__(self, value):
        limit_value = self.limit_callable()
        params = {'limit_value': limit_value, 'value': value}
        if self.compare(value, limit_value):
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            (self.limit_callable == other.limit_callable)
            and (self.message == other.message)
            and (self.code == other.code)
        )


@deconstructible
class MaxCallableValidator(BaseCallableValidator):
    compare = lambda self, a, b: a > b
    message = _('Ensure this value is less than or equal to %(limit_value)s.')
    code = 'max_value'


@deconstructible
class MinCallableValidator(BaseCallableValidator):
    compare = lambda self, a, b: a < b
    message = _('Ensure this value is greater than or equal to %(limit_value)s.')
    code = 'min_value'
