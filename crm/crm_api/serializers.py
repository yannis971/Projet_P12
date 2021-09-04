from django.shortcuts import get_object_or_404

from rest_framework import serializers

from django.contrib.auth.models import User

from crm_api.models import (Client, Contract, Event, EventStatus,
                            SalesContact, StaffContact, SupportContact)


class ClientSerializer(serializers.ModelSerializer):
    """
    Client serializer
    """
    sales_contact_id = serializers.ReadOnlyField(source='sales_contact.id')

    class Meta:
        model = Client
        fields = ['first_name', 'last_name',
                  'email', 'phone', 'mobile', 'sales_contact_id']

    def save(self, **kwargs):
        the_sales_contact = get_object_or_404(SalesContact, pk=self._kwargs['data']['sales_contact_id'])
        return super().save(sales_contact=the_sales_contact)


class ContractSerializer(serializers.ModelSerializer):
    """
    Contract serializer
    """
    sales_contact_id = serializers.ReadOnlyField(source='sales_contact.id')
    client_id = serializers.ReadOnlyField(source='client.id')

    class Meta:
        model = Contract
        fields = ['sales_contact_id', 'client_id',
                  'status', 'amount', 'payment_due']

    def save(self, **kwargs):
        the_sales_contact = get_object_or_404(SalesContact, pk=self._kwargs['data']['sales_contact_id'])
        the_client = get_object_or_404(Client, pk=self._kwargs['data']['client_id'])
        return super().save(sales_contact=the_sales_contact, client=the_client)


class EventSerializer(serializers.ModelSerializer):
    """
    Event serializer
    """
    support_contact_id = serializers.ReadOnlyField(source='support_contact.id')
    client_id = serializers.ReadOnlyField(source='client.id')
    event_status_id = serializers.ReadOnlyField(source='event_status.id')

    class Meta:
        model = Event
        fields = ['client_id', 'support_contact_id',
                  'event_status_id', 'attendees', 'event_date', 'notes']

    def save(self, **kwargs):
        the_support_contact = get_object_or_404(SupportContact, pk=self._kwargs['data']['support_contact_id'])
        the_client = get_object_or_404(Client, pk=self._kwargs['data']['client_id'])
        the_event_status = get_object_or_404(EventStatus, pk=self._kwargs['data']['event_status_id'])
        return super().save(support_contact=the_support_contact, client=the_client, event_status=the_event_status)


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    class Meta:
        model = User
        fields = ['username', 'password']

"""
class SalesContactSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')

    class Meta:
        model = SalesContact
        fields = ['user_id', 'username', 'password']

    def save(self, **kwargs):
        the_user = get_object_or_404(User, pk=self._kwargs['data']['user_id'])
        return super().save(user=the_user)
"""


class SalesContactSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')

    class Meta:
        model = SupportContact
        fields = ['user_id', 'username', 'password']

    def save(self, **kwargs):
        the_user = get_object_or_404(User, pk=self._kwargs['data']['user_id'])
        return super().save(user=the_user)


class SupportContactSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')

    class Meta:
        model = SupportContact
        fields = ['user_id', 'username', 'password']

    def save(self, **kwargs):
        the_user = get_object_or_404(User, pk=self._kwargs['data']['user_id'])
        return super().save(user=the_user)


class StaffContactSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')

    class Meta:
        model = StaffContact
        fields = ['user_id', 'username', 'password']

    def save(self, **kwargs):
        the_user = get_object_or_404(User, pk=self._kwargs['data']['user_id'])
        return super().save(user=the_user)
