#-*- codng: utf-8 -*-

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from oauth2app.models import Client


@login_required
def profile(request):
    user = request.user
    return render_to_response(
        'accounts/profile.html',
        {
            "clients": Client.objects.filter(user=user)
        },
        RequestContext(request)
    )


def homepage(request):
    return render_to_response(
        'accounts/homepage.html',
        RequestContext(request)
    )
