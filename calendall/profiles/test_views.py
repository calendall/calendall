from datetime import timedelta

from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from .models import CalendallUser
from .forms import CalendallUserCreateForm
from .views import CalendallUserCreate


@override_settings(DEBUG=True)  # For the static ones
class TestCalendallUserCreation(TestCase):

    def setUp(self):

        self.url = reverse("profiles:calendalluser_create")

        self.users = (
            {
                'username': "batman",
                'email': "darkknight@gmail.com",
                'password': 'I\'mBatman',
                'password_verification': 'I\'mBatman'
            },
            {
                'username': "woverine",
                'email': "wolf&scars@gmail.com",
                'password': 'claws1600',
                'password_verification': 'claws1600'
            },
            {
                'username': "BlackWidow",
                'email': "blackwidow@gmail.com",
                'password': 'Чёрная вдова',
                'password_verification': 'Чёрная вдова'
            },
            {
                'username': "MazingerZ",
                'email': "MazingerZ@gmail.com",
                'password': 'マジンガ',
                'password_verification': 'マジンガ'
            },
        )

    def test_correct_creation(self):
        c = Client()

        for i in self.users:
            response = c.post(self.url, i)

            self.assertRedirects(response, self.url)
            self.assertEqual(response.status_code, 302)

            u = CalendallUser.objects.filter(username=i['username'])[0]
            self.assertEqual(u.email, i['email'])
            self.assertTrue(u.check_password(i['password']))
            self.assertTrue(u.check_password(i['password_verification']))

        self.assertEqual(CalendallUser.objects.count(), len(self.users))

    def test_autologin_in_correct_creation(self):
        c = Client()

        for i in self.users:
            response = c.post(self.url, i)

            self.assertRedirects(response, self.url)
            self.assertEqual(response.status_code, 302)

            # Check auto login verying the session
            u = CalendallUser.objects.filter(username=i['username'])[0]
            self.assertEqual(response.client.session['_auth_user_id'], u.pk)

    #def test_username_required(self):
    #    c = Client()
#
#    #    for i in self.users:
#    #        del i['username']
#    #        response = c.post(self.url, i)
#
#    #        self.assertEqual(response.status_code, 200)
#
#    #        self.assertFormError(response,
#    #                             CalendallUserCreateForm,
#    #                             'username',
    #                             'This field is required.')
