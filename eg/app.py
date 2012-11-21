# Copyright (c) Paul Tagliamonte <paultag@debian.org>, 2012 under the terms
# and conditions of the Expat license, a copy of which should be given to you
# with the source of this application.

from flask import Flask, redirect, session, request, render_template
from sanction.client import Client


BASE = 'http://localhost:8000'
SELF = 'http://localhost:5000'
REDIRECT_URL = '%s/recv' % (SELF)

AUTH_BASE = '%s/oauth2' % (BASE)
API_BASE = '%s/api' % (BASE)

AUTH_URL = '%s/authorize' % (AUTH_BASE)
TOKEN_URL = '%s/token' % (AUTH_BASE)

CLIENT_ID = '450cd1a10f9163f2fd2bb90410f1a1'
CLIENT_KEY = 'fdb7ad0d1465d524fa941239392d7d'

SCOPE = ('all',)

def shoe(refresh_token=None):
    c = Client(
        auth_endpoint=AUTH_URL,
        token_endpoint=TOKEN_URL,
        resource_endpoint=API_BASE,
        redirect_uri=REDIRECT_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_KEY
    )
    if refresh_token:
        c.request_token(refresh_token)
    return c


app = Flask(__name__)
app.secret_key = 'foo bar baz'


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login")
def login():
    return redirect(shoe().auth_uri(SCOPE))


@app.route("/recv")
def recv():
    if 'code' in request.args:
        c = shoe()
        params = {}
        for arg in request.args:
            params[arg] = request.args[arg]
        c.request_token(**params)

        session['refresh_token'] = c.refresh_token
        session['code'] = params['code']

        return redirect('/info')
    return render_template('error.html', args=request.args)


@app.route("/info")
def info():
    c = shoe()
    c.request_token(
        grant_type='refresh_token',
        refresh_token=session['refresh_token']
    )
    email = c.request('/email')
    return str(email)


if __name__ == "__main__":
    app.debug = True
    app.run()
