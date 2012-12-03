#-*- codng: utf-8 -*-

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.http import urlquote
from oauth2app.authorize import get_authorized_clients
from oauth2app.models import Client, Code, AccessToken
from shoelace.apps.accounts.forms import SignupForm
from django.contrib.auth.views import login as login_view
from urlparse import urlparse, parse_qs
from shoelace.apps.oauth2.models import ClientProfile


def login_shim(request, **kwargs):
    request.shoelace = {
        "client": None,
        "client_profile": None
    }
    if 'next' in request.GET:
        next_vals = urlparse(request.GET['next'])
        if hasattr(next_vals, 'query'):
            params = parse_qs(next_vals.query)
            if 'client_id' in params and len(params['client_id']) > 0:
                client_id = params['client_id'][0]  # Is this right?
                try:
                    client = Client.objects.get(key=client_id)
                    request.shoelace['client'] = client
                    client_profile = ClientProfile.objects.get(client=client)
                    request.shoelace['client_profile'] = client_profile
                except Client.DoesNotExist:
                    pass

    return login_view(request, **kwargs)


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

            u.first_name = form.cleaned_data['first_name']
            u.last_name = form.cleaned_data['last_name']

            u.save()

            # log the user in by default
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password'])
            login(request, new_user)

            if not request.POST['next']:
                return redirect(reverse('profile'))
            else:
                return redirect(request.POST['next'])
    else:
        form = SignupForm()

    return render_to_response(
        'accounts/signup.html', {
            'form': form,
            'next': request.GET.get('next')
        }, RequestContext(request)
    )
