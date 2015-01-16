from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^register$', views.CalendallUserCreate.as_view(),
        name="calendalluser_create"),

    url(r'^login$', views.Login.as_view(), name="login"),
    url(r'^logout$', views.Logout.as_view(), name="logout"),
    url(r'^validate/(?P<username>[a-zA-Z0-9\-]{1,30})/(?P<token>[a-f0-9]{32})$',
        views.Validate.as_view(), name="validate"),

    url(r'^settings/profile$', views.ProfileSettings.as_view(),
        name="profile_settings"),

)
