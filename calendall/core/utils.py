from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

import premailer


def send_templated_email(template_name, context, subject, sender, receivers):
    """
        Sends a templated email. The template_name shoudln't have  the prefix,
        will load the .txt and the .html templates with the name
    """
    # Load templates
    txt_render = render_to_string(template_name + ".txt", context)
    html_render = render_to_string(template_name + ".html", context)

    # Inline CSS and links
    html_render = premailer.transform(html_render,
                                      base_url="http://" + settings.DOMAIN)

    send_mail(
        html_message=html_render,
        message=txt_render,
        subject=subject,
        from_email=sender,
        recipient_list=receivers,
        fail_silently=False)
