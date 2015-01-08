from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy

from .models import CalendallUser
from .forms import CalendallUserCreateForm


class CalendallUserCreate(CreateView):
    model = CalendallUser
    fields = ['username', 'email', 'password']
    form_class = CalendallUserCreateForm
    template_name = "profiles/profiles_calendalluser_create.html"
    success_url = reverse_lazy('profiles:calendalluser_create')

    def get_context_data(self, **kwargs):
        print(kwargs['form'].fields['username'].required)
        return super().get_context_data(**kwargs)
