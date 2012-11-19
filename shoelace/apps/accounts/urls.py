from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    (
        r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'accounts/login.html'
        }
    ),
)
