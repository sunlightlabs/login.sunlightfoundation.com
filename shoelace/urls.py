from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^oauth2/',   include('shoelace.apps.oauth2.urls')),
    (r'^api/',      include('shoelace.apps.api.urls')),
    (r'^accounts/', include('shoelace.apps.accounts.urls')),
    (r'^admin/',    include(admin.site.urls)),
    (r'^$',         'shoelace.apps.accounts.views.homepage'),
)

