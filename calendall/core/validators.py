from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import pytz


def validate_timezone(value):
    if value not in pytz.common_timezones:
        raise ValidationError(_('Invalid value: %(value)s'),
                              code='invalid',
                              params={'value': value})
