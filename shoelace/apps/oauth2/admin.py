from django.contrib import admin
from oauth2app.models import Client, AccessRange
from shoelace.apps.oauth2.models import ClientProfile


class ClientAdmin(admin.ModelAdmin):
    exclude = ('redirect_uri',)

admin.site.register(Client, ClientAdmin)


class ClientProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(ClientProfile, ClientProfileAdmin)


class AccessRangeAdmin(admin.ModelAdmin):
    pass

admin.site.register(AccessRange, AccessRangeAdmin)
