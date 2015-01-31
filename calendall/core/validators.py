import logging
import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import pytz

log = logging.getLogger(__name__)
color_regex = re.compile("^([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$")


def validate_timezone(value):
    log.debug("Validate '{0}' timezone".format(value))

    if value not in pytz.common_timezones:
        log.error("Invalida timezone: '{0}'".format(value))
        raise ValidationError(_('Invalid value: %(value)s'),
                              code='invalid',
                              params={'value': value})


def validate_color(value):
    log.debug("Validate '{0}' color".format(value))

    if not color_regex.match(value):
        log.error("Invalida color: '{0}'".format(value))
        raise ValidationError(_('Invalid value: %(value)s'),
                              code='invalid',
                              params={'value': value})