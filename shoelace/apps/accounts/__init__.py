from django.contrib.auth.forms import AuthenticationForm

AuthenticationForm.base_fields['username'].max_length = 100
AuthenticationForm.base_fields['username'].widget.attrs['maxlength'] = 100
AuthenticationForm.base_fields['username'].validators[0].limit_value = 100
