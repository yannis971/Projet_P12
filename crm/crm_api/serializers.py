from django.conf import settings
from django.core.validators import EmailValidator, MaxLengthValidator, ProhibitNullCharactersValidator
from rest_framework import serializers
from crm_api.models import SalesContact, SupportContact, Client, Contract, Event


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
                }
            }


    def validate(self, data):
        try:
            first_name = self._kwargs['data']['first_name']
            last_name = self._kwargs['data']['last_name']
            email = self._kwargs['data']['email']
            sales_contact_id = self._kwargs['data']['sales_contact_id']
        except KeyError:
            message = "first_name, last_name, email and sales_contact_id are mandatory fields"
            raise serializers.ValidationError(message)
        else:
            email_validator = EmailValidator()
            email_validator(email)
        return data


class ContractSerializer(serializers.ModelSerializer):
    """
    Contract serializer
    """
    sales_contact_id = serializers.ReadOnlyField(source='sales_contact.id')
    client_id = serializers.ReadOnlyField(source='client.id')
    class Meta:
        model = Contract
        fields = ['sales_contact_id', 'client_id', 'status', 'amont', 'payment_due']

    def validate(self, data):
        if all((field in self._kwargs['data'] for field in self.fields)):
            pass
        else:
            message = "first_name, last_name, email and sales_contact_id are mandatory fields"
            raise serializers.ValidationError(message)
        return data


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

    def validate(self, data):
        if all((field in self._kwargs['data'] for field in self.fields)):
            pass
        else:
            message = "first_name, last_name, email and sales_contact_id are mandatory fields"
            raise serializers.ValidationError(message)
        return data
