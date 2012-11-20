from django.contrib import admin
from oauth2app.models import Client


class ClientAdmin(admin.ModelAdmin):
    exclude = ('redirect_uri',)

admin.site.register(Client, ClientAdmin)
