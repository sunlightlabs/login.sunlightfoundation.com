from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(
        r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'accounts/login.html'
        },
    ),
    url(
        r'^logout/$',
        'django.contrib.auth.views.logout',
        {
            'template_name': 'accounts/logout.html'
        },
    ),
    url(
        r'^profile/$',
        'shoelace.apps.accounts.views.profile',
        name='profile'
    ),
    url(
        r'^revoke/(?P<app_id>.*)/$',
        'shoelace.apps.accounts.views.revoke',
        name='revoke'
    )
)
