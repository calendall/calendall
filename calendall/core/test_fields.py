from django.db import models
from django.utils import timezone
from django.test import TestCase
from django.test.utils import override_settings

from .fields.dates import AutoDateTimeField
from .test_utils import TestFieldModel


class ModifiedModel(TestFieldModel):
    title = models.CharField(max_length=20)
    last_modified = AutoDateTimeField(default=timezone.now)


@override_settings(DEBUG=True)
class DateFieldsTestCase(TestCase):

    def setUp(self):
        ModifiedModel.create_table()

    def tearDown(self):
        ModifiedModel.delete_table()

    def test_auto_datetime_field(self):
        instance = ModifiedModel.objects.create(title="test")
        loaded = ModifiedModel.objects.get()
        self.assertIsNotNone(loaded)

        date_old = loaded.last_modified
        for i in range(20):
            instance.title = "title{0}".format(i)
            instance.save()
            date_new = ModifiedModel.objects.all()[0].last_modified
            self.assertGreater(date_new, date_old)
            date_old = date_new
