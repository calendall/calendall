from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy

from .models import CalendallUser


class CalendallUserCreate(CreateView):
    model = CalendallUser
    fields = ['username', 'email', 'password']
    template_name = "profiles/profiles_calendalluser_create.html"
    success_url = reverse_lazy('profiles:calendalluser_create')
