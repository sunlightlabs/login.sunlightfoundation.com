#-*- coding: utf-8 -*-


from oauth2app.authenticate import JSONAuthenticator, AuthenticationException


def userinfo(request):
    authenticator = JSONAuthenticator()  # XXX: Scope?
    try:
        authenticator.validate(request)
    except AuthenticationException:
        return authenticator.error_response()

    return authenticator.response({
        "email": authenticator.user.email,
        "username": authenticator.user.username,
        "first_name": authenticator.user.first_name,
        "last_name": authenticator.user.last_name,
        "is_staff": authenticator.user.is_staff,
        "is_active": authenticator.user.is_active,
        "is_superuser": authenticator.user.is_superuser
    })
