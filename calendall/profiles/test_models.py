import uuid
from datetime import timedelta

from django.utils import timezone
from django.test import TestCase

from .models import CalendallUser


# Simple tests, this shouldn't be neccessary, the ORM is already tested
# by Django :P
class CalendallUserTestCase(TestCase):

    def setUp(self):
        self.data = [
            {
                "username": "Batman",
                "password": "I'm batman",
                "first_name": "Bruce",
                "last_name": "Wayne",
                "email": "darkknight@gmail.com",
                "timezone": "America/New_York",
                "reset_token": str(uuid.uuid4()).replace("-", ""),
                "reset_expiration": timezone.now() + timedelta(minutes=20),
                "validation_token": str(uuid.uuid4()).replace("-", ""),
                "validated": False,
                "url": "https://darkknight.com",
                "location": "Gotham city",
            },
            {
                "username": "Spiderman",
                "password": "I Love spiders",
                "first_name": "Peter",
                "last_name": "Parker",
                "email": "spidy@gmail.com",
                "timezone": "America/New_York",
                "reset_token": str(uuid.uuid4()).replace("-", ""),
                "reset_expiration": timezone.now() + timedelta(minutes=20),
                "validation_token": str(uuid.uuid4()).replace("-", ""),
                "validated": True,
                "url": "http://spiderstories.com",
                "location": "NY",
            },
            {
                "username": "ProfesorX",
                "password": "Mutants & humans",
                "first_name": "Charles",
                "last_name": "Xavier",
                "email": "boldAndMutant@gmail.com",
                "timezone": "America/New_York",
                "reset_token": str(uuid.uuid4()).replace("-", ""),
                "reset_expiration": timezone.now() + timedelta(minutes=20),
                "validation_token": str(uuid.uuid4()).replace("-", ""),
                "validated": True,
                "url": "http://www.mutantunited.net",
                "location": "X Mansion",
            },
        ]
        for i in self.data:
            u = CalendallUser(**i)
            u.set_password(i['password'])
            u.save()

    def check_attrs_helper(self, objects, data=None):
        """Checks by default in the data param, if not then in the global"""

        if not data:
            data = [{} for i in range(len(objects))]

        for k, v in enumerate(objects):
            self.assertEqual(v.username, data[k].get('username',
                                                     self.data[k]['username']))
            self.assertTrue(v.check_password(
                            data[k].get('password', self.data[k]['password'])))
            self.assertEqual(v.first_name,
                             data[k].get('first_name',
                                         self.data[k]['first_name']))
            self.assertEqual(v.last_name,
                             data[k].get('last_name',
                                         self.data[k]['last_name']))
            self.assertEqual(v.email, data[k].get('email',
                                                  self.data[k]['email']))
            self.assertEqual(v.timezone, data[k].get('timezone',
                                                     self.data[k]['timezone']))
            self.assertEqual(v.reset_token,
                             str(data[k].get('reset_token',
                                             self.data[k]['reset_token'])))
            self.assertEqual(v.reset_expiration,
                             data[k].get('reset_expiration',
                                         self.data[k]['reset_expiration']))
            self.assertEqual(v.validated,
                             data[k].get('validated',
                                         self.data[k]['validated']))
            self.assertEqual(v.validation_token,
                             data[k].get('validation_token',
                                         self.data[k]['validation_token']))
            self.assertEqual(v.url, data[k].get('url', self.data[k]['url']))
            self.assertEqual(v.location, data[k].get('location',
                             self.data[k]['location']))

    def test_save(self):
        """test save calendall user object"""
        self.assertEqual(CalendallUser.objects.count(), len(self.data))

    def test_retrieve(self):
        """Test retieval of all users"""
        users = CalendallUser.objects.all()
        self.check_attrs_helper(users)

    def test_update(self):
        email_suffix = ".test"
        users = CalendallUser.objects.all()
        data = []

        for i in users:
            i.email += email_suffix
            data.append({"email": i.email})
            i.save()

        self.check_attrs_helper(CalendallUser.objects.all(), data)

    def test_delete(self):
        users = CalendallUser.objects.all()
        for i in users:
            i.delete()

        self.assertEqual(CalendallUser.objects.count(), 0)
