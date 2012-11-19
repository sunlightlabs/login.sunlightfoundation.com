#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('shoelace.apps.api.views',
    (r'^email/?$',                 'email')
)
