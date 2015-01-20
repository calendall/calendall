from datetime import timedelta
import logging
import uuid

from django.conf import settings
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, FormView, RedirectView
from django.views.generic.edit import UpdateView

from .models import CalendallUser
from .forms import (CalendallUserCreateForm, LoginForm, ProfileSettingsForm,
                    AccountSettingsForm, AskPasswordResetForm,
                    PasswordResetForm)

from core import utils
from core.views import LoginRequiredMixin

log = logging.getLogger(__name__)


class CalendallUserCreate(CreateView):
    model = CalendallUser
    fields = ['username', 'email', 'password']
    form_class = CalendallUserCreateForm
    template_name = "profiles/profiles_calendalluser_create.html"
    success_url = reverse_lazy('profiles:calendalluser_create')

    # Auto generate the validation token
    def form_valid(self, form):
        form.instance.validation_token = str(uuid.uuid4()).replace("-", "")
        return super().form_valid(form)

    def get_success_url(self):
        # Auto log in process:
        # Check password & user is ok (this isn't neccesary)
        user = authenticate(username=self.request.POST['username'],
                            password=self.request.POST['password'])
        if user is not None:
            if user.is_active:
                log.debug("Auto login '{0}'".format(user))
                login(self.request, user)

        # Send welcome email
        utils.send_templated_email("profiles/emails/profiles_email_welcome",
                                   self.get_context_data(),
                                   _("Welcome to Calendall"),
                                   settings.EMAIL_SUPPORT,
                                   (user.email,),
                                   self.request)

        # Send validation email
        utils.send_templated_email("profiles/emails/profiles_email_validation",
                                   self.get_context_data(),
                                   _("Validate your Calendall account"),
                                   settings.EMAIL_NOREPLY,
                                   (user.email,),
                                   self.request)

        return self.success_url

    @method_decorator(sensitive_post_parameters('password',
                                                'password_verification'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class Login(FormView):

    form_class = LoginForm
    template_name = "profiles/profiles_login.html"
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
        return super().form_valid(form)

    def get_success_url(self):
        # First check POST
        next_url = self.request.POST.get('next', None)

        if not next_url:
            next_url = self.request.GET.get('next', None)

        if next_url:
            self.success_url = next_url

        return self.success_url

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super().dispatch(request, *args, **kwargs)


class Logout(LoginRequiredMixin, RedirectView):

    url = settings.LOGIN_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, _("successfuly logged out"))
        return super().get(request, *args, **kwargs)


class Validate(RedirectView):
    url = settings.LOGIN_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        error = True

        # Check if the values is correct
        try:
            u = CalendallUser.objects.get(username=self.kwargs['username'])

            if u.validated:
                log.debug("User '{0}' already validated".format(u))
                messages.info(request, _("Account already validated"))
                error = False

            elif u.validation_token == self.kwargs['token']:
                u.validated = True
                u.save()
                log.info("User '{0}' validated".format(u))
                messages.success(request, _("successfuly account validated"))
                error = False

        except CalendallUser.DoesNotExist:
            pass  # This will be error

        if error:
            log.debug(
                "Error validating user '{0}'".format(self.kwargs['username']))
            messages.error(request, _("Error validating the account"))

        return super().get(request, *args, **kwargs)


class ProfileSettings(LoginRequiredMixin, UpdateView):
    model = CalendallUser
    form_class = ProfileSettingsForm
    template_name = "profiles/profiles_profile_settings.html"
    success_url = reverse_lazy('profiles:profile_settings')

    # With this we don't need the pk in the url
    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # Set the timezone of the user in the session
        self.request.session['user-tz'] = form.cleaned_data['timezone']
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Profile updated"))
        return super().get_success_url()


class AccountSettings(LoginRequiredMixin, UpdateView):
    model = CalendallUser
    form_class = AccountSettingsForm
    template_name = "profiles/profiles_account_settings.html"
    success_url = reverse_lazy('profiles:account_settings')

    # we need request in the form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        result = super().form_valid(form)
        # Don't logout the user (>= 1.7)
        update_session_auth_hash(self.request, self.request.user)
        return result

    # With this we don't need the pk in the url
    def get_object(self):
        return self.request.user

    def get_success_url(self):
        messages.success(self.request, _("Account updated"))
        return super().get_success_url()


class AskPasswordReset(FormView):

    form_class = AskPasswordResetForm
    template_name = "profiles/profiles_ask_password_reset.html"
    success_url = settings.LOGIN_REDIRECT_URL

    # Prepopulate the login if logged
    def get_initial(self):
        initial_data = super().get_initial()
        try:
            initial_data['email'] = self.request.user.email
        except AttributeError:
            pass  # anonymous user

        return initial_data

    def form_valid(self, form):

        # Get user
        context_data = self.get_context_data()
        u = CalendallUser.objects.get(
            email=form.cleaned_data['email'])

        # Create the token & date
        u.reset_token = str(uuid.uuid4()).replace("-", "")
        expiration_time = timezone.now()
        # Add expiration  time
        u.reset_expiration = expiration_time + timedelta(
            seconds=settings.PASSWORD_RESET_MAX_SECONDS)

        u.save()
        context_data['user'] = u

        # Send email
        utils.send_templated_email("profiles/emails/profiles_email_password_reset",
                                   context_data,
                                   _("Please reset your password"),
                                   settings.EMAIL_NOREPLY,
                                   (form.cleaned_data['email'],),
                                   self.request)

        messages.success(self.request, _("Email sent with the instructions"))

        return super().form_valid(form)


class PasswordReset(UpdateView):

    model = CalendallUser
    form_class = PasswordResetForm
    template_name = "profiles/profiles_password_reset.html"
    success_url = settings.LOGIN_REDIRECT_URL
    validation_error_url = reverse_lazy("profiles:ask_password_reset")

    def dispatch(self, request, *args, **kwargs):
        try:
            username = self.kwargs.get('username', "")
            token = self.kwargs.get('token', "")
            self.user = CalendallUser.objects.get(username=username)
            # First check the token is ok
            if token == self.user.reset_token and\
               self.user.reset_expiration >= timezone.now():
                return super().dispatch(request, *args, **kwargs)

        except CalendallUser.DoesNotExist:
            pass  # show error but not a clue about the user inexstence

        log.debug("Error resettings password for: {0}".format(username))
        messages.error(self.request, _("It looks like you clicked on an invalid password reset link or it expired. Please try again."))
        return redirect(self.validation_error_url)

    # With this we don't need the pk in the url
    def get_object(self):
        return self.user

    def form_valid(self, form):
        # Don't allow reset again
        self.user.reset_token = ""
        self.user.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _("Account updated"))
        return super().get_success_url()
