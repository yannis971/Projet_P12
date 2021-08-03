from django.core.validators import EmailValidator
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

    def validate(self, data):
        try:
            first_name = self._kwargs['data']['first_name']
            last_name = self._kwargs['data']['last_name']
            email = self._kwargs['data']['email']
        except KeyError:
            message = "first_name, last_name and email are mandatory fields"
            raise serializers.ValidationError(message)
        else:
            email_validator = EmailValidator()
            email_validator(email)
        return data
