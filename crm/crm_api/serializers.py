from django.conf import settings
from django.core.validators import DecimalValidator, EmailValidator, integer_validator, MaxLengthValidator, ProhibitNullCharactersValidator
from rest_framework import serializers
from crm_api.models import SalesContact, SupportContact, Client, Contract, Event
from crm_api.validators import DateTimeValidator


class ClientSerializer(serializers.ModelSerializer):
    """
    Client serializer
    """
    sales_contact_id = serializers.ReadOnlyField(source='sales_contact.id')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone', 'mobile', 'sales_contact_id']
        if settings.DEBUG == True:
            extra_kwargs = {
                'first_name': {
                    'validators': [MaxLengthValidator, ProhibitNullCharactersValidator]
                },
                'last_name': {
                    'validators': [MaxLengthValidator, ProhibitNullCharactersValidator]
                },
                'email': {
                    'validators': [MaxLengthValidator, ProhibitNullCharactersValidator, EmailValidator]
                },
                'phone': {
                    'validators': [MaxLengthValidator, ]
                },
                'mobile': {
                    'validators': [MaxLengthValidator, ]
                },
                'sales_contact_id': {
                    'validators': [integer_validator, ]
                },
            }


class ContractSerializer(serializers.ModelSerializer):
    """
    Contract serializer
    """
    sales_contact_id = serializers.ReadOnlyField(source='sales_contact.id')
    client_id = serializers.ReadOnlyField(source='client.id')

    class Meta:
        model = Contract
        fields = ['sales_contact_id', 'client_id', 'status', 'amount', 'payment_due']
        if settings.DEBUG == True:
            extra_kwargs = {
                'sales_contact_id': {
                    'validators': [integer_validator, ]
                },
                'client_id': {
                    'validators': [integer_validator, ]
                },
                'amount': {
                    'validators': [DecimalValidator(max_digits=9, decimal_places=2), ]
                },
                'payment_due': {
                    'validators': [DateTimeValidator(), ]
                },
            }


class EventSerializer(serializers.ModelSerializer):
    """
    Event serializer
    """
    support_contact_id = serializers.ReadOnlyField(source='support_contact.id')
    client_id = serializers.ReadOnlyField(source='client.id')
    event_status_id = serializers.ReadOnlyField(source='event_status.id')

    class Meta:
        model = Event
        fields = ['client_id', 'support_contact_id', 'event_status_id', 'attendees', 'event_date', 'notes']
        if settings.DEBUG == True:
            extra_kwargs = {
                'client_id': {
                    'validators': [integer_validator, ]
                },
                'support_contact_id': {
                    'validators': [integer_validator, ]
                },
                'event_status_id': {
                    'validators': [integer_validator, ]
                },
                'attendees': {
                    'validators': [integer_validator, ]
                },
                'notes': {
                    'validators': [MaxLengthValidator, ]
                },
            }
