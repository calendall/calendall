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
    # Tokens are uuid without slashes
    reset_token = models.CharField(_("reset token"),
                                   max_length=32,
                                   blank=True)
    reset_expiration = models.DateTimeField(_("reset token expiration"),
                                            null=True)

    validated = models.BooleanField(_("User account validated"), default=False)
    validation_token = models.CharField(_("User account validation token"),
                                        max_length=32,
                                        blank=True)

    def __str__(self):
        return self.email
