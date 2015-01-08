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

        self.fields['username'].required = True
        self.fields['password_verification'] = forms.CharField(
            label=_('Confirm your password'), max_length=128, required=True)

    def clean_email(self):
        # TODO: Check email exists
        pass

    def clean_username(self):
        # TODO: Check username exists
        pass

    def clean(self):
        # TODO: Check Both passwords are the same
        pass
