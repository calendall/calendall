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
        # TODO: Check email exists
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        # TODO: Check username exists
        return username

    def clean(self):
        # TODO: Check Both passwords are the same
        pass
