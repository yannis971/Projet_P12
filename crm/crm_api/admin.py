from django.contrib import admin

from crm_api.models import SalesContact, StaffContact, SupportContact, Client, Contract, Event, EventStatus
# Register your models here.


class ClientAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'email', 'sales_contact')
    list_filter = ('sales_contact',)
    search_fields = ('first_name', 'last_name', 'email')


class ContractAdmin(admin.ModelAdmin):

    list_display = ('sales_contact', 'client', 'status', 'amount', 'payment_due')
    list_filter = ('sales_contact', 'client')


class EventAdmin(admin.ModelAdmin):

    list_display = ('client', 'support_contact', 'event_status', 'attendees', 'event_date')
    list_filter = ('client', 'support_contact', 'event_status')
    search_fields = ('notes',)


admin.site.register(SalesContact)
admin.site.register(StaffContact)
admin.site.register(SupportContact)
admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventStatus)
