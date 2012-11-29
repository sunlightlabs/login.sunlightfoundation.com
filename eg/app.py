# Copyright (c) Paul Tagliamonte <paultag@debian.org>, 2012 under the terms
# and conditions of the Expat license, a copy of which should be given to you
# with the source of this application.

from flask import Flask, redirect, session, request, render_template
from sanction.client import Client
from urllib2 import HTTPError


BASE = 'http://localhost:8000'
SELF = 'http://localhost:5000'
REDIRECT_URL = '%s/recv' % (SELF)

AUTH_BASE = '%s/oauth2' % (BASE)
API_BASE = '%s/api' % (BASE)

AUTH_URL = '%s/authorize' % (AUTH_BASE)
TOKEN_URL = '%s/token' % (AUTH_BASE)

CLIENT_ID = '774e87cb9e65bc3a040d1e5f87534a'
CLIENT_KEY = '441c0a3d5ccb0f988dac5605ba6614'

SCOPE = ('all',)

def shoe():
    if 'shoe_client' in session:
        c = session['shoe_client']
    else:
        c = Client(
            auth_endpoint=AUTH_URL,
            token_endpoint=TOKEN_URL,
            resource_endpoint=API_BASE,
            redirect_uri=REDIRECT_URL,
            client_id=CLIENT_ID,
            client_secret=CLIENT_KEY
        )

    if hasattr(c, 'refresh_token'):
        c.request_token(grant_type="refresh_token",
                        refresh_token=c.refresh_token)
        # XXX: Refactor this to be only when we're expired or something.

    session['shoe_client'] = c
    return c


app = Flask(__name__)
app.secret_key = 'foo bar baz'


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login")
def login():
    try:
        return redirect(shoe().auth_uri(SCOPE))
    except HTTPError:  # Stale something or other. Just kick it.
        session.pop('shoe_client')
        return redirect("/login")


@app.route("/recv")
def recv():
    if 'code' in request.args:
        c = shoe()
        params = {}
        for arg in request.args:
            params[arg] = request.args[arg]

        c.request_token(**params)
        session['shoe_client'] = c

        return redirect('/info')
    return render_template('error.html', args=request.args)


@app.route("/info")
def info():
    c = shoe()
    email = c.request('/userinfo')
    return str(email)


if __name__ == "__main__":
    app.debug = True
    app.run()
