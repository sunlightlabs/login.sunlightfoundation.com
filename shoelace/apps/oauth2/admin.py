from django.contrib import admin
from oauth2app.models import Client, AccessRange


class ClientAdmin(admin.ModelAdmin):
    exclude = ('redirect_uri',)

admin.site.register(Client, ClientAdmin)


class AccessRangeAdmin(admin.ModelAdmin):
    pass

admin.site.register(AccessRange, AccessRangeAdmin)
