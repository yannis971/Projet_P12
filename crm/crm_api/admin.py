from django.contrib import admin

from crm_api.models import SalesContact, StaffContact, SupportContact, Client, Contract, Event, EventStatus
# Register your models here.

admin.site.register(SalesContact)
admin.site.register(StaffContact)
admin.site.register(SupportContact)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
admin.site.register(EventStatus)
