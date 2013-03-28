from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^oauth2/', include('shoelace.apps.oauth2.urls')),
    url(r'^api/', include('shoelace.apps.api.urls')),
    url(r'^accounts/', include('shoelace.apps.accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('sfapp.urls')),
    url(r'^$', 'shoelace.apps.accounts.views.homepage'),
)
