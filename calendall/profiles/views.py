import logging
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout

from .models import CalendallUser
from .forms import CalendallUserCreateForm


log = logging.getLogger(__name__)


class CalendallUserCreate(CreateView):
    model = CalendallUser
    fields = ['username', 'email', 'password']
    form_class = CalendallUserCreateForm
    template_name = "profiles/profiles_calendalluser_create.html"
    success_url = reverse_lazy('profiles:calendalluser_create')

    def get_success_url(self):
        # Auto log in process:
        # Check password & use is ok (this isn't neccesary)
        user = authenticate(username=self.request.POST['username'],
                            password=self.request.POST['password'])
        if user is not None:
            if user.is_active:
                log.debug("Auto login '{0}'".format(user))
                login(self.request, user)

        return self.success_url
