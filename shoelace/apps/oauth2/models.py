from django.db import models
from oauth2app.models import Client


class ClientProfile(models.Model):
    client = models.OneToOneField(Client)

    template_slug = models.CharField(max_length=30)
    image_url = models.CharField(max_length=256)
    signup_text = models.TextField()
    login_text = models.TextField()
