from django.db import models
from django.utils import timezone
from django.test import TestCase

from .fields.dates import AutoDateTimeField


class DateFieldsTestCase(TestCase):

    # custom model class to test the field
    class ModifiedModel(models.Model):
        title = models.CharField(max_length=20)
        last_modified = AutoDateTimeField(default=timezone.now)

    def test_auto_datetime_field(self):
        pass
        #instance = self.__class__ModifiedModel.objects.create(title="test")
        #loaded = self.__class__ModifiedModel.objects.get()
        #self.assertIsNotNone(loaded.last_modified)

        #for i in range(20):
        #    date_old = self.m.last_modified
        #    self.m.title = "title{0}".format(i)
        #    self.m.save()
        #    self.assertGreater(self.object.all()[0].last_modified, date_old)
