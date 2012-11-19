#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
        (r'^missing_redirect/?$',  'shoelace.apps.oauth2.views.missing_redirect'),
        (r'^authorize/?$',         'shoelace.apps.oauth2.views.authorize'),
        (r'^token/?$',             'oauth2app.token.handler'),
)
