from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.utils import timezone

from profiles.models import CalendallUser


@override_settings(DEBUG=True)
class TestTimezoneMiddleware(TestCase):

    def setUp(self):
        self.url = reverse("profiles:profile_settings")

        self.data = {
            'username': "batman",
            'email': "darkknight@gmail.com",
            'password': 'I\'mBatman123',
        }

        self.user = CalendallUser(**self.data)
        self.user.set_password(self.data['password'])
        self.user.save()

    def test_timezone_middleware_logged_out(self):
        c = Client()
        c.get(self.url)
        self.assertEqual(timezone.get_current_timezone_name(),
                         settings.TIME_ZONE)

    def test_timezone_middleware_logged_from_session(self):
        c = Client()
        c.login(username=self.data['username'],
                password=self.data['password'])
        tz = "Europe/Madrid"
        session = c.session
        session["user-tz"] = tz
        session.save()
        c.get(self.url)
        self.assertEqual(timezone.get_current_timezone_name(), tz)

    def test_timezone_middleware_logged_from_database(self):
        c = Client()
        c.login(username=self.data['username'],
                password=self.data['password'])

        tz = "Europe/Amsterdam"
        self.user.timezone = tz
        self.user.save()
        c.session["user-tz"] = tz
        c.session.save()
        c.get(self.url)
        self.assertEqual(timezone.get_current_timezone_name(), tz)
