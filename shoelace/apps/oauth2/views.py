#-*- codng: utf-8 -*-

from shoelace.apps.oauth2.models import ClientProfile


from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import get_authorized_clients
from oauth2app.authorize import (Authorizer, MissingRedirectURI,
                                 AuthorizationException)
from .forms import AuthorizeForm


@login_required
def missing_redirect(request):
    return render_to_response(
        'oauth2/missing_redirect.html',
        {},
        RequestContext(request))


@login_required
def authorize(request):
    authorizer = Authorizer()
    try:
        authorizer.validate(request)
    except MissingRedirectURI:
        return HttpResponseRedirect("/oauth2/missing_redirect")  # XXX: Fix.
    except AuthorizationException:
        # The request is malformed or invalid. Automatically
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    if request.method == 'GET':
        # Make sure the authorizer has validated before requesting the client
        # or access_ranges as otherwise they will be None.
        if settings.SHOELACE_QUERY_AUTH_ALWAYS:
            return authorizer.grant_redirect()


        if settings.SHOELACE_QUERY_AUTH_FIRST_LOGIN:
            if authorizer.client.id in [
                x.id for x in get_authorized_clients(request.user)
            ]:
                return authorizer.grant_redirect()

        profile = ClientProfile.objects.filter(client=authorizer.client)
        profile = None if len(profile) <= 0 else profile[0]

        template = {
            "client": authorizer.client,
            "access_ranges": authorizer.access_ranges,
            "GET": request.GET,
            "profile": profile
        }
        return render_to_response(
            'oauth2/authorize.html',
            template,
            RequestContext(request)
        )
    elif request.method == 'POST':
        form = AuthorizeForm(request.POST)
        if form.is_valid():
            if request.POST.get("connect") == "Yes":
                return authorizer.grant_redirect()
            else:
                return authorizer.error_redirect()
    return HttpResponseRedirect("/")
