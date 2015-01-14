from django.core import mail
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.utils import override_settings

from .utils import send_templated_email


TEST_EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


@override_settings(DEBUG=True,
                   EMAIL_BACKEND=TEST_EMAIL_BACKEND)
class TestEmailUtils(TestCase):

    def test_send_email(self):
        data = {
            "subject": "I'm Batman",
            "context": {
                "user": "Joker"
            },
            "template_name": "tests/emails/tests_email_test",
            "sender": "batman@gmail.com",
            "receivers": ("joker@gmail.com",),
        }

        result_txt = render_to_string(data['template_name'] + ".txt",
                                      data['context'])
        result_html = render_to_string(data['template_name'] + ".html",
                                       data['context'])

        send_templated_email(**data)
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, data['subject'])
        self.assertEquals(mail.outbox[0].from_email, data['sender'])
        self.assertEquals(mail.outbox[0].body, result_txt)
        self.assertEquals(mail.outbox[0].alternatives[0][0], result_html)
        self.assertEquals(data['receivers'][0], mail.outbox[0].recipients()[0])
