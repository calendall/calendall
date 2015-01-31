from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
import pytz

from profiles.models import CalendallUser
from core.validators import validate_timezone, validate_color


TIMEZONES = [(tz, tz) for tz in pytz.common_timezones]


@python_2_unicode_compatible
class Calendar(models.Model):

    owner = models.ForeignKey(CalendallUser)
    timezone = models.CharField(_("Calendar timezone"),
                                max_length=40,  # Max is 30, but 10 extra
                                choices=TIMEZONES,
                                default='UTC',
                                validators=[validate_timezone])

    name = models.CharField(_("Calendar name"),
                            max_length=32)

    description = models.TextField(_("Calendar description"),
                                   blank=True)

    color = models.CharField(_("Calendar name"),
                             max_length=6,
                             validators=[validate_color])

    icon = models.URLField(_("Calendar icon"),
                           blank=True)

    def __str__(self):
        return self.name


#@python_2_unicode_compatible
#class Event(models.Model):
#
#    calendar = models.ForeignKey(Calendar)
#    # rule
#
#
#@python_2_unicode_compatible
#class Rule(models.Model):
#
#    event = models.OneToOneField(Event)
#