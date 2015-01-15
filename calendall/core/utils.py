import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template import RequestContext
from django.template.loader import render_to_string

import premailer


log = logging.getLogger(__name__)


def send_templated_email(template_name, context, subject, sender, receivers,
                         request=None):
    """
        Sends a templated email. The template_name shoudln't have  the prefix,
        will load the .txt and the .html templates with the name
    """

    request_context = None
    if request:
        # Is more handy to use 'request' instance in render_to_string:
        # https://github.com/django/django/commit/eaa1a22341aef5b92f5c3cd682f01e61c4159262
        request_context = RequestContext(request)
        base_url = request.build_absolute_uri()
    else:
        base_url = "http://" + settings.DOMAIN

    # Load templates
    txt_render = render_to_string(template_name + ".txt", context,
                                  context_instance=request_context)
    html_render = render_to_string(template_name + ".html", context,
                                   context_instance=request_context)

    # Inline CSS and links
    # If we are testing don't use premail:
    if not settings.TESTING:
        html_render = premailer.transform(html_render, base_url=base_url)

    send_mail(
        html_message=html_render,
        message=txt_render,
        subject=subject,
        from_email=sender,
        recipient_list=receivers,
        fail_silently=False)

    log.info("Sent email '{0}' to '{1}'".format(subject, receivers))
