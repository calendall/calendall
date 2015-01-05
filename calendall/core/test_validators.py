import random
import uuid

from django.test import TestCase
from django.core.exceptions import ValidationError
import pytz

from .validators import validate_timezone


class TimezoneValidatorTestCase(TestCase):

    def setUp(self):
        self.data = [
            ("Europe/Madrid", True),
            ("Inferno", False),
            ("UTC", True),
            ("Heaven", False),
            ("America/New_York", True),
            ("Flatland", False),
        ]

    def test_all_correct(self):
        for i in pytz.common_timezones:
            validate_timezone(i)

    def test_all_wrong(self):
        for i in pytz.common_timezones:
            with self.assertRaises(ValidationError):
                validate_timezone(i + "_bad")

    def test_predefined_data(self):
        for i in self.data:
            if i[1]:
                validate_timezone(i[0])
            else:
                self.assertRaises(ValidationError, validate_timezone, (i[0]))

    def test_random_data(self):
        number_tests = 200

        for i in range(number_tests):
            if i % 2 == 0:  # True value
                validate_timezone(random.choice(pytz.common_timezones))
            else:  # False value
                self.assertRaises(ValidationError,
                                  validate_timezone,
                                  str(uuid.uuid4()))
