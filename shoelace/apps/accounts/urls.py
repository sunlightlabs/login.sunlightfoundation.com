from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    # contrib.auth views
    url(
        r'^login/$',
#        'django.contrib.auth.views.login',
        'shoelace.apps.accounts.views.login_shim',  # this calls the django view.
        { 'template_name': 'accounts/login.html' },
        name='login',
    ),
    url(
        r'^logout/$',
#        'django.contrib.auth.views.logout',
        'shoelace.apps.accounts.views.logout_shim',
        { 'template_name': 'accounts/logout.html' },
        name='logout',
    ),
    url(
        r'^password_change/$',
        'django.contrib.auth.views.password_change',
        {'template_name': 'accounts/password_change_form.html',
        },
        name='password_change',
    ),
    url(
        r'^password_change_done/$',
        'django.contrib.auth.views.password_change_done',
        { 'template_name': 'accounts/password_change_done.html' },
        name='password_change_done',
    ),
    url(
        r'^password_reset/$',
        'django.contrib.auth.views.password_reset',
        {'template_name': 'accounts/password_reset_form.html',
         'email_template_name': 'accounts/password_reset_email.html',
         'subject_template_name': 'accounts/password_reset_subject.txt',
        },
        name='password_reset',
    ),
    url(
        r'^password_reset_done/$',
        'django.contrib.auth.views.password_reset_done',
        { 'template_name': 'accounts/password_reset_done.html' },
        name='password_reset_done',
    ),
    url(
        r'^password_reset_confirm/$',
        'django.contrib.auth.views.password_reset_confirm',
        { 'template_name': 'accounts/password_reset_confirm.html' },
        name='password_reset_confirm',
    ),
    url(
        r'^password_reset_complete/$',
        'django.contrib.auth.views.password_reset_complete',
        { 'template_name': 'accounts/password_reset_complete.html' },
        name='password_reset_complete',
    ),
    # custom views
    url(
        r'^profile/$',
        'shoelace.apps.accounts.views.profile',
        name='profile'
    ),
    url(
        r'^revoke/(?P<app_id>.*)/$',
        'shoelace.apps.accounts.views.revoke',
        name='revoke'
    ),
    url(
        r'^signup/$',
        'shoelace.apps.accounts.views.signup',
        name='signup'
    )
)
