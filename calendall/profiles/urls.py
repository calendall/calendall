from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^register$', views.CalendallUserCreate.as_view(),
        name="calendalluser_create"),
)
