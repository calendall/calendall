import logging

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from .models import CalendallUser
from . import utils


log = logging.getLogger(__name__)


# Profile form mixins
class NewPasswordMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password_verification'] = forms.CharField(
            label=_('Confirm your password'), max_length=128, required=True)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not utils.valid_password(password):
            msg = _("minimun 7 characters, one letter and one number")
            raise forms.ValidationError(msg)

        return password

    def clean(self):
        self.cleaned_data = super().clean()
        password = self.cleaned_data.get('password', "")
        password_verification = self.cleaned_data.get('password_verification', "")

        if password and password_verification and password != password_verification:
            log.debug("password '{0}' and '{1}'' differ".format(
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


# Forms
class CalendallUserCreateForm(NewPasswordMixin, forms.ModelForm):

    class Meta:
        model = CalendallUser
        fields = ["email", "username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        if utils.email_exists(email):
            log.debug("email '{0}' already taken".format(email))
            raise forms.ValidationError(_("already taken"))

        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        if not utils.valid_username(username):
            log.debug("username '{0}' not ^.(?<!\-)[a-zA-Z0-9\-]{{1,29}}$".format(username))
            raise forms.ValidationError(_("May only contain alphanumeric characters or dashes and cannot begin with a dash"))

        # Check username exists
        if utils.username_exists(username):
            log.debug("username '{0}' already taken".format(username))
            raise forms.ValidationError(_("already taken"))

        return username


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Username or Email")

    # Reimplement the login to allow email and username login
    def clean(self):
        # Don't do this because email is in the username field and will get error
        # self.cleaned_data = super().clean()
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        dont_check = False

        if username_or_email and password:
            # Check if is an email
            if "@" in username_or_email:
                # Validate the email
                try:
                    validate_email(username_or_email)
                    username = CalendallUser.objects.get(
                        email=username_or_email).username
                except (forms.ValidationError, CalendallUser.DoesNotExist):
                    dont_check = True
            else:
                username = username_or_email

            # Do not check if not a valid email
            if not dont_check:
                self.user_cache = authenticate(username=username,
                                               password=password)
            if self.user_cache is None:
                log.debug("Invalid login for user '{0}'".format(
                    username_or_email))
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class ProfileSettingsForm(forms.ModelForm):

    class Meta:
        model = CalendallUser
        fields = ["first_name", "last_name", "url", "location", "timezone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].label = _("URL")
        self.fields['location'].label = _("Location")
        self.fields['timezone'].help_text = _("Select timezone")


class AccountSettingsForm(NewPasswordMixin, forms.ModelForm):

    class Meta:
        model = CalendallUser
        fields = ["password"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.fields['old_password'] = forms.CharField(
            label=_('Old password'), max_length=128, required=True)
        self.fields['password'].label = _("Old password")
        self.fields['password'].required = True
        self.fields['password_verification'].label = _('Confirm new password')
        self.fields['password'].required = True

    def clean_old_password(self):
        password = self.cleaned_data.get('old_password', "")
        if password and not utils.valid_password(password):
            msg = _("minimun 7 characters, one letter and one number")
            raise forms.ValidationError(msg)

        return password

    def clean(self):
        old_password = self.cleaned_data.get('old_password', "")

        if old_password:
            if not self.request.user.check_password(old_password):
                msg = _("Old password isn't valid")
                self.add_error('old_password', msg)
                raise forms.ValidationError(msg)

        self.cleaned_data = super().clean()

        return self.cleaned_data


class AskPasswordResetForm(forms.ModelForm):

    class Meta:
        model = CalendallUser
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email', "")
        if not utils.email_exists(email):
            log.debug("error reseting password for: {0}".format(email))
            raise forms.ValidationError(_("Can't find that email, sorry"))

        return email


class PasswordResetForm(NewPasswordMixin, forms.ModelForm):

    class Meta:
        model = CalendallUser
        fields = ["password"]
