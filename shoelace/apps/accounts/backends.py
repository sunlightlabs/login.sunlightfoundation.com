from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """ very simple class to authenticate w/ email instead of username """

    def authenticate(self, username, password):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
