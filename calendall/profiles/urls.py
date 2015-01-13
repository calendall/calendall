from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^register$', views.CalendallUserCreate.as_view(),
        name="calendalluser_create"),

    url(r'^login$', views.Login.as_view(), name="login"),
    url(r'^logout$', views.Logout.as_view(), name="logout"),
)
