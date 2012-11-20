# Copyright (c) Paul Tagliamonte <paultag@debian.org>, 2012 under the terms
# and conditions of the Expat license, a copy of which should be given to you
# with the source of this application.

from flask import Flask, redirect, session, request
from sanction.client import Client


BASE = 'http://localhost:8000'
SELF = 'http://localhost:5000'
REDIRECT_URL = '%s/recv' % (SELF)

AUTH_BASE = '%s/oauth2' % (BASE)
API_BASE = '%s/api' % (BASE)

AUTH_URL = '%s/authorize' % (AUTH_BASE)
TOKEN_URL = '%s/token' % (AUTH_BASE)

CLIENT_ID = '3aa23807530031a618987d4ba6033e'
CLIENT_KEY = 'cef4a23ca68e61dbc6e5d1bf7b381c'

SCOPE = ()

shoelace = Client(
    auth_endpoint=AUTH_URL,
    token_endpoint=TOKEN_URL,
    resource_endpoint=API_BASE,
    redirect_uri=REDIRECT_URL,
    client_id=CLIENT_ID,
    client_secret=CLIENT_KEY
)

app = Flask(__name__)
app.secret_key = 'foo bar baz'


@app.route("/")
def index():
    return redirect("/login")


@app.route("/login")
def login():
    return redirect(shoelace.auth_uri(SCOPE))


@app.route("/recv")
def recv():
    c = shoelace
    params = {}
    for arg in request.args:
        params[arg] = request.args[arg]
    c.request_token(**params)
    rc = Client(
        token_endpoint=c.token_endpoint,
        client_id=c.client_id,
        client_secret=c.client_secret,
        resource_endpoint=c.resource_endpoint
    )

    rc.request_token(
        grant_type="refresh_token",
        refresh_token=c.refresh_token
    )

    session['refresh_token'] = rc.refresh_token
    session['code'] = params['code']

    return redirect('/info')


@app.route("/info")
def info():
    email = shoelace.request('/email')
    return str(email)


if __name__ == "__main__":
    app.debug = True
    app.run()
