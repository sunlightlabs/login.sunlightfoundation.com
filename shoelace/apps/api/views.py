#-*- coding: utf-8 -*-


from oauth2app.authenticate import JSONAuthenticator, AuthenticationException


def email(request):
    authenticator = JSONAuthenticator()  # XXX: Scope?
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()

    return authenticator.response({
        "email": authenticator.user.email
    })
