from django import forms
from django.core import validators
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User


class SignupForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(30)
    last_name = forms.CharField(30)
    password = forms.CharField(widget=PasswordInput())
    password2 = forms.CharField(label='Confirm Password',
                                widget=PasswordInput())

    def clean_email(self):
        try:
            User.objects.get(email=self.data['email'])
        except User.DoesNotExist:
            return self.data['email']
        raise validators.ValidationError(
            'The email "%s" is already taken.' % (self.data['email'])
        )

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean(self,*args, **kwargs):
        self.clean_email()
        self.clean_password()
        return super(SignupForm, self).clean(*args, **kwargs)
