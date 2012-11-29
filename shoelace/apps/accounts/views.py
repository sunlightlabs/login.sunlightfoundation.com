#-*- codng: utf-8 -*-

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from oauth2app.models import Client, Code, AccessToken
from oauth2app.authorize import get_authorized_clients
from shoelace.apps.accounts.forms import SignupForm
from django.contrib.auth.models import User


@login_required
def profile(request):
    user = request.user
    authed = []

    for client in get_authorized_clients(user):
        token = AccessToken.objects.filter(
            user=user,
            client=client
        ).order_by('-expire').select_related()[0]

        authed.append({
            "client": client,
            "last_token": token
        })

    return render_to_response(
        'accounts/profile.html', {
            "clients": Client.objects.filter(user=user),
            "authed_apps": authed

#             "codes": Code.objects.filter(
#                 user=user
#             ).order_by('-expire').select_related(),
#             "tokens": AccessToken.objects.filter(
#                 user=user
#             ).order_by('-expire').select_related(),

        }, RequestContext(request)
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


def signup(request):
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return redirect(reverse('profile'))

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(
                form.cleaned_data['email'][:30],  # Hack. Username.
                form.cleaned_data['email'],
                form.cleaned_data['password'],
            )

            u.first_name = form.cleaned_data['first_name'],
            u.last_name = form.cleaned_data['last_name']

            u.is_active = False
            u.save()

            return redirect(reverse('profile'))
    else:
        form = SignupForm()

    return render_to_response(
        'accounts/signup.html', {
            'form': form
        }, RequestContext(request)
    )
