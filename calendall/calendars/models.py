from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from profiles.models import CalendallUser


@python_2_unicode_compatible
class Calendar(models.Model):

    owner =  models.ForeignKey(CalendallUser)

#    def __str__(self):
#        return self.email
#


@python_2_unicode_compatible
class Event(models.Model):

    calendar = models.ForeignKey(Calendar)
    # rule


@python_2_unicode_compatible
class Rule(models.Model):

    event = models.OneToOneField(Event)
