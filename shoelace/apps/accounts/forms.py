from django import forms
from django.core import validators
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User


class SignupForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(30)
    last_name = forms.CharField(30)
    password = forms.CharField(widget=PasswordInput())
    password2 = forms.CharField(widget=PasswordInput())

    def is_valid_email(self, field_data, all_data):
        try:
            User.objects.get(email=field_data)
        except User.DoesNotExist:
            return
        raise validators.ValidationError('The email "%s" is already taken.' % field_data)
