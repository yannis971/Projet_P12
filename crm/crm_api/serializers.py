from rest_framework import serializers

from crm_api.models import (Client, Contract, Event, SalesContact,
                            StaffContact, SupportContact, User)


class ClientSerializer(serializers.ModelSerializer):
    """
    Client serializer
    """
    sales_contact_id = serializers.ReadOnlyField(source='sales_contact.sales_contact_id')

    class Meta:
        model = Client
        fields = ['client_id', 'first_name', 'last_name',
                  'email', 'phone', 'mobile', 'sales_contact_id']


class ContractSerializer(serializers.ModelSerializer):
    """
    Contract serializer
    """
    sales_contact_id = serializers.ReadOnlyField(source='sales_contact.sales_contact_id')
    client_id = serializers.ReadOnlyField(source='client.client_id')

    class Meta:
        model = Contract
        fields = ['contract_id', 'sales_contact_id', 'client_id',
                  'status', 'amount', 'payment_due']


class EventSerializer(serializers.ModelSerializer):
    """
    Event serializer
    """
    support_contact_id = serializers.ReadOnlyField(source='support_contact.support_contact_id')
    client_id = serializers.ReadOnlyField(source='client.client_id')
    event_status_id = serializers.ReadOnlyField(source='event_status.event_status_id')

    class Meta:
        model = Event
        fields = ['event_id', 'client_id', 'support_contact_id',
                  'event_status_id', 'attendees', 'event_date', 'notes']


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password']


class SalesContactSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.user_id')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')

    class Meta:
        model = SalesContact
        fields = ['sales_contact_id', 'user_id', 'username', 'password']


class SupportContactSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.user_id')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')

    class Meta:
        model = SupportContact
        fields = ['support_contact_id', 'user_id', 'username', 'password']


class StaffContactSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.user_id')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')

    class Meta:
        model = StaffContact
        fields = ['staff_contact_id', 'user_id', 'username', 'password']
