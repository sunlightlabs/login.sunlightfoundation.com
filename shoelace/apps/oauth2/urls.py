#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(
        r'^missing_redirect/?$',
        'shoelace.apps.oauth2.views.missing_redirect'
    ),
    url(r'^authorize/?$', 'shoelace.apps.oauth2.views.authorize'),
    url(r'^token/?$', 'oauth2app.token.handler'),
)
