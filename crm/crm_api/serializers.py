from django.conf import settings
from django.core.validators import DecimalValidator, EmailValidator, integer_validator, MaxLengthValidator, ProhibitNullCharactersValidator
from rest_framework import serializers
from django.contrib.auth.models import User
from crm_api.models import SalesContact, SupportContact, Client, Contract, Event


class ClientSerializer(serializers.ModelSerializer):
    """
    Client serializer
    """
    sales_contact_id = serializers.ReadOnlyField(source='sales_contact.id')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone', 'mobile', 'sales_contact_id']


class ContractSerializer(serializers.ModelSerializer):
    """
    Contract serializer
    """
    sales_contact_id = serializers.ReadOnlyField(source='sales_contact.id')
    client_id = serializers.ReadOnlyField(source='client.id')

    class Meta:
        model = Contract
        fields = ['sales_contact_id', 'client_id', 'status', 'amount', 'payment_due']


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


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    class Meta:
        model = User
        fields = ['username', 'password']