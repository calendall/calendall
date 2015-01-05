from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
import pytz

from core.validators import validate_timezone

TIMEZONES = [(tz, tz) for tz in pytz.common_timezones]


@python_2_unicode_compatible
class CalendallUser(AbstractUser):

    timezone = models.CharField(_("User timezone"),
                                max_length=40,  # Max is 30, but 10 extra
                                choices=TIMEZONES,
                                default='UTC',
                                validators=[validate_timezone])
    reset_token = models.CharField(_("reset token"),
                                   max_length=36,
                                   blank=True)
    reset_expiration = models.DateTimeField(_("reset token expiration"),
                                            null=True)

    def __str__(self):
        return self.email
