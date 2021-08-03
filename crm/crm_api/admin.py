from django.contrib import admin

from crm_api.models import SalesContact, SupportContact, Client, Contract, Event
# Register your models here.

admin.site.register(SalesContact)
admin.site.register(SupportContact)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
