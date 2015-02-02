from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
import pytz

from profiles.models import CalendallUser
from core.validators import validate_timezone, validate_color
from core.fields.dates import AutoDateTimeField

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
                            max_length=100)

    description = models.TextField(_("Calendar description"),
                                   blank=True)

    color = models.CharField(_("Calendar name"),
                             max_length=6,
                             validators=[validate_color])

    icon = models.URLField(_("Calendar icon"),
                           blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Event(models.Model):

    calendar = models.ForeignKey(Calendar)
    start = models.DateTimeField(_("Event start date"))
    end = models.DateTimeField(_("Event start date"))
    full_day = models.BooleanField(_("Event uses full day notation"),
                                   default=False),
    created = models.DateTimeField(_("Event start date"),
                                   default=timezone.now)
    modified = AutoDateTimeField(_("Event last modified date"),
                                 default=timezone.now)

    uid = models.CharField(_("Event uuid"),
                           max_length=100)
    summary = models.CharField(_("Event summary"),
                               max_length=100)
    description = models.TextField(_("Event description"),
                                   blank=True)
    sequence = models.IntegerField(_("Event version"),
                                   default=0)
    location = models.CharField(_("Event location"),
                                max_length=200)
    # rule


#@python_2_unicode_compatible
#class Rule(models.Model):
#
#    event = models.OneToOneField(Event)
#