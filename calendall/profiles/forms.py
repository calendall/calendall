import re
import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import CalendallUser

log = logging.getLogger(__name__)


class CalendallUserCreateForm(forms.ModelForm):

    class Meta:
        model = CalendallUser
        fields = ["email", "username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = True
        self.fields['password_verification'] = forms.CharField(
            label=_('Confirm your password'), max_length=128, required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if CalendallUser.objects.filter(email=email).exists():
            log.debug("email '{0}' already taken".format(email))
            raise forms.ValidationError(_("already taken"))

        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        # Check username is: A-Z, a-z and only dashes
        # Can't start wiht a dash
        # 30 max
        r = re.compile("^.(?<!\-)[a-zA-Z0-9\-]{1,29}$")
        if not r.match(username):
            log.debug("username '{0}' not ^.(?<!\-)[a-zA-Z0-9\-]{{1,29}}$".format(username))
            raise forms.ValidationError(_("May only contain alphanumeric characters or dashes and cannot begin with a dash"))

        # Check username exists
        if CalendallUser.objects.filter(username=username).exists():
            log.debug("username '{0}' already taken".format(username))
            raise forms.ValidationError(_("already taken"))
        return username

    def clean(self):
        password = self.cleaned_data.get('password', "")
        password_verification = self.cleaned_data.get('password_verification', "")

        if password != password_verification:
            log.debug("password '{0}' and {1} differ".format(
                password, password_verification))

            msg = _("doesn't match the confirmation")
            self.add_error('password', msg)
            self.add_error('password_verification', msg)
            raise forms.ValidationError(msg)

        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
