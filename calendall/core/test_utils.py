from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.utils import override_settings
from unittest import mock
import premailer

from .utils import send_templated_email
from .mock_utils import local_url_loader


@mock.patch.object(premailer.Premailer, '_load_external',
                   side_effect=local_url_loader)
@override_settings(DEBUG=True,
                   EMAIL_BACKEND=settings.TEST_EMAIL_BACKEND)
class TestEmailUtils(TestCase):

    def test_send_email(self, mock_method):
        data = {
            "subject": "I'm Batman",
            "context": {
                "user": "Joker",
                "domain": settings.DOMAIN
            },
            "template_name": "tests/emails/tests_email_test",
            "sender": "batman@gmail.com",
            "receivers": ("joker@gmail.com",),
        }

        result_txt = render_to_string(data['template_name'] + ".txt",
                                      data['context'])
        result_html = render_to_string(data['template_name'] + ".html",
                                       data['context'])

        # Don't use premailer in tests, because of static retrieval errors
        result_html = premailer.transform(result_html,
                                          base_url="http://" + settings.DOMAIN)

        send_templated_email(**data)
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, data['subject'])
        self.assertEquals(mail.outbox[0].from_email, data['sender'])
        self.assertEquals(mail.outbox[0].body, result_txt)
        self.assertEquals(mail.outbox[0].alternatives[0][0], result_html)
        self.assertEquals(data['receivers'][0], mail.outbox[0].recipients()[0])
