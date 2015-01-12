import logging
from django.views.generic import CreateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from .models import CalendallUser
from .forms import CalendallUserCreateForm, LoginForm


log = logging.getLogger(__name__)


class CalendallUserCreate(CreateView):
    model = CalendallUser
    fields = ['username', 'email', 'password']
    form_class = CalendallUserCreateForm
    template_name = "profiles/profiles_calendalluser_create.html"
    success_url = reverse_lazy('profiles:calendalluser_create')

    def get_success_url(self):
        # Auto log in process:
        # Check password & user is ok (this isn't neccesary)
        user = authenticate(username=self.request.POST['username'],
                            password=self.request.POST['password'])
        if user is not None:
            if user.is_active:
                log.debug("Auto login '{0}'".format(user))
                login(self.request, user)

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
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.set_test_cookie()
        return super(Login, self).dispatch(request, *args, **kwargs)
