import uuid
from datetime import timedelta

from django.utils import timezone
from django.test import TestCase

from profiles.models import CalendallUser
from .models import Calendar


# Simple tests, this shouldn't be neccessary, the ORM is already tested
# by Django :P
class CalendallUserTestCase(TestCase):

    def setUp(self):
        user = {
            "username": "Batman",
            "password": "I'm batman",
            "email": "darkknight@gmail.com",
        }

        self.u = CalendallUser(**user)
        self.u.set_password(user['password'])
        self.u.save()

        self.data = [
            {
                'owner': self.u,
                'timezone': 'UTC',
                'name': 'Jail calendar',
                'description': 'Days when I jailed bad people',
                'color': 'FAFAFA',
                'icon': 'https://mysttics.com/123456789',
            },
            {
                'owner': self.u,
                'timezone': 'Europe/Madrid',
                'name': 'Superhero birthdays calendar',
                'description': 'Birthdays of other superheroes',
                'color': '4BFEA1',
                'icon': 'https://mysttics.com/5324132',
            },
            {
                'owner': self.u,
                'timezone': 'Europe/London',
                'name': 'Jail calendar',
                'description': 'Days when I jailed bad people',
                'color': 'FAFAFA',
                'icon': 'https://mysttics.com/123456789',
            }
        ]

        for i in self.data:
            Calendar(**i).save()

    def check_attrs_helper(self, objects, data=None):
        """Checks by default in the data param, if not then in the global"""

        if not data:
            data = [{} for i in range(len(objects))]

        for k, v in enumerate(objects):
            self.assertEqual(v.owner, data[k].get('owner',
                                                  self.data[k]['owner']))

            self.assertEqual(v.timezone, data[k].get('timezone',
                                                     self.data[k]['timezone']))

            self.assertEqual(v.name, data[k].get('name',
                                                 self.data[k]['name']))

            self.assertEqual(v.description, data[k].get('description',
                             self.data[k]['description']))

            self.assertEqual(v.color, data[k].get('color',
                                                  self.data[k]['color']))

            self.assertEqual(v.icon, data[k].get('icon',
                                                 self.data[k]['icon']))

    def test_save(self):
        """test save caledar object"""
        self.assertEqual(Calendar.objects.count(), len(self.data))

    def test_retrieve(self):
        """Test retieval of all calendars"""
        calendars = Calendar.objects.all()
        self.check_attrs_helper(calendars)

    def test_update(self):
        name_suffix = ".test"
        calendars = Calendar.objects.all()
        data = []

        for i in calendars:
            i.name += name_suffix
            data.append({"name": i.name})
            i.save()

        self.check_attrs_helper(Calendar.objects.all(), data)

    def test_delete(self):
        calendars = Calendar.objects.all()
        for i in calendars:
            i.delete()

        self.assertEqual(Calendar.objects.count(), 0)
