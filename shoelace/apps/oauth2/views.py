#-*- codng: utf-8 -*-


from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from oauth2app.authorize import Authorizer, MissingRedirectURI, AuthorizationException
from oauth2app.authorize import UnvalidatedRequest, UnauthenticatedUser
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
    except MissingRedirectURI, e:
        return HttpResponseRedirect("/oauth2/missing_redirect")  # XXX: Fix this
    except AuthorizationException, e:
        # The request is malformed or invalid. Automatically
        # redirects to the provided redirect URL.
        return authorizer.error_redirect()
    if request.method == 'GET':
        # Make sure the authorizer has validated before requesting the client
        # or access_ranges as otherwise they will be None.
        template = {
            "client":authorizer.client,
            "access_ranges":authorizer.access_ranges}
        template["form"] = AuthorizeForm()
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
