#-*- codng: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from oauth2app.models import Client, Code, AccessToken
from oauth2app.authorize import get_authorized_clients


@login_required
def profile(request):
    user = request.user
    return render_to_response(
        'accounts/profile.html',
        {
            "clients": Client.objects.filter(user=user),

            "codes": Code.objects.filter(
                user=user).order_by('-expire').select_related(),

            "access_tokens": AccessToken.objects.filter(
                user=user).order_by('-expire').select_related(),
            "authed_apps": get_authorized_clients(user)
        },
        RequestContext(request)
    )


def homepage(request):
    return render_to_response(
        'accounts/homepage.html',
        RequestContext(request)
    )


def revoke(request, app_id):
    client = Client.objects.filter(id=app_id)[0]  # XXX: Saner error.
    tokens = AccessToken.objects.filter(client=client)
    [t.delete() for t in tokens]
    return redirect(reverse('profile'))
