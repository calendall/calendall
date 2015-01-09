from django.test import TestCase


from .templatetags import core_tags


class CoreTagsTestCase(TestCase):

    def setUp(self):
        self.data = [
            {
                'strs': (
                    'first error',
                    'second error',
                    'third error',
                    'fourth error',
                    ),
                'join_word': None,
                'last_join_word': ' and ',
                'result': 'first error, second error, third error and fourth error',
            },
            {
                'strs': (
                    'first error',
                    'second error',
                    'third error',
                    'fourth error',
                    ),
                'join_word': ' and ',
                'last_join_word': None,
                'result': 'first error and second error and third error and fourth error',
            },
            {
                'strs': (
                    'first error',
                    'second error',
                    'third error',
                    'fourth error',
                    ),
                'join_word': '-',
                'last_join_word': '|',
                'result': 'first error-second error-third error|fourth error',
            },
            {
                'strs': (
                    'first error',
                    ),
                'join_word': None,
                'last_join_word': None,
                'result': 'first error',
            }
        ]

    def test_join_errors_string_creation(self):

        for i in self.data:

            self.assertEqual(
                core_tags.join_strings(i['strs'],
                                       i['last_join_word'],
                                       i['join_word']),
                i['result'])
