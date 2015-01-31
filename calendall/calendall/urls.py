from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from profiles import urls as profile_urls
from calendars import urls as calendar_urls


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^p/', include(profile_urls, namespace="profiles")),
    url(r'^c/', include(calendar_urls, namespace="calendars")),
    url(r'^admin/', include(admin.site.urls)),
)

# In production static stuff should be server by http server
# static handles automatically if the DEBUG is True
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
