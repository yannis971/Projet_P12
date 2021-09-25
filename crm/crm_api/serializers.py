"""
Module serializers.py
"""

from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from crm_api.models import (
    Client,
    Contract,
    Event,
    EventStatus,
    SalesContact,
    StaffContact,
    SupportContact,
)


class GroupSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    class Meta:
        """ MetaClass with model and fields"""
        model = Group
        fields = [
            "name",
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """

    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        """ MetaClass with model and fields"""
        model = User
        fields = ["username", "password", "groups"]


class SalesContactSerializer(serializers.ModelSerializer):
    """
    SalesContact serializer
    """
    user = UserSerializer(many=False)

    class Meta:
        """ MetaClass with model and fields"""
        model = SalesContact
        fields = "__all__"

    def create(self, validated_data):
        """
        Method to create the instance of User
        then the instance of SalesContact
        """
        user_data = validated_data.pop("user", None)
        user_data["is_staff"] = True
        user = User.objects.create_user(**user_data)
        return SalesContact.objects.create(user=user)

    def update(self, instance, validated_data):
        """
        Method to update the instance of user
        """
        user_data = validated_data.pop("user")
        user_instance = User.objects.get(username=user_data["username"])
        user_instance.set_password(user_data["password"])
        user_instance.save()
        instance.user = user_instance
        return instance


class SupportContactSerializer(serializers.ModelSerializer):
    """
    SupportContact serializer
    """
    user = UserSerializer(many=False)

    class Meta:
        """ MetaClass with model and fields"""
        model = SupportContact
        fields = "__all__"

    def create(self, validated_data):
        """
        Method to create the instance of User
        then the instance of SupportContact
        """
        user_data = validated_data.pop("user", None)
        user_data["is_staff"] = True
        user = User.objects.create_user(**user_data)
        return SupportContact.objects.create(user=user)

    def update(self, instance, validated_data):
        """
        Method to update the instance of user
        """
        user_data = validated_data.pop("user")
        user_instance = User.objects.get(username=user_data["username"])
        user_instance.set_password(user_data["password"])
        user_instance.save()
        instance.user = user_instance
        return instance


class StaffContactSerializer(serializers.ModelSerializer):
    """
    StaffContact serializer
    """
    user = UserSerializer(many=False)

    class Meta:
        """ MetaClass with model and fields"""
        model = StaffContact
        fields = "__all__"

    def create(self, validated_data):
        """
        Method to create the instance of User
        then the instance of StaffsContact
        """
        user_data = validated_data.pop("user", None)
        user_data["is_staff"] = True
        user = User.objects.create_user(**user_data)
        return StaffContact.objects.create(user=user)

    def update(self, instance, validated_data):
        """
        Method to update the instance of user
        """
        user_data = validated_data.pop("user")
        user_instance = User.objects.get(username=user_data["username"])
        user_instance.set_password(user_data["password"])
        user_instance.save()
        instance.user = user_instance
        return instance


class ClientSerializer(serializers.ModelSerializer):
    """
    Client serializer
    """

    sales_contact_id = serializers.ReadOnlyField(source="sales_contact.id")

    class Meta:
        """ MetaClass with model and excluded fields"""
        model = Client
        exclude = [
            "sales_contact",
        ]

    def validate(self, data):
        """
        Method to validate the data to serialize
        """
        if "sales_contact_id" not in self._kwargs["data"]:
            raise serializers.ValidationError(
                detail="sales_contact_id is required in data", code="invalid"
            )
        return data

    def save(self, **kwargs):
        """
        Method to save the instance of Client
        """
        the_sales_contact = get_object_or_404(
            SalesContact, pk=self._kwargs["data"]["sales_contact_id"]
        )
        return super().save(sales_contact=the_sales_contact)


class ContractSerializer(serializers.ModelSerializer):
    """
    Contract serializer
    """

    sales_contact_id = serializers.ReadOnlyField(source="sales_contact.id")
    client_id = serializers.ReadOnlyField(source="client.id")

    class Meta:
        """ MetaClass with model and excluded fields"""
        model = Contract
        exclude = ["sales_contact", "client"]

    def validate(self, data):
        """
        Method to validate the data to serialize
        """
        if "sales_contact_id" not in self._kwargs["data"]:
            raise serializers.ValidationError(
                detail="sales_contact_id is required in data", code="invalid"
            )
        elif "client_id" not in self._kwargs["data"]:
            raise serializers.ValidationError(
                detail="client_id is required in data", code="invalid"
            )
        return data

    def save(self, **kwargs):
        """
        Method to save the instance of Contract
        """
        the_sales_contact = get_object_or_404(
            SalesContact, pk=self._kwargs["data"]["sales_contact_id"]
        )
        the_client = get_object_or_404(Client,
                                       pk=self._kwargs["data"]["client_id"])
        return super().save(sales_contact=the_sales_contact, client=the_client)


class EventStatusSerializer(serializers.ModelSerializer):
    """
    EventStatus Serializer
    """
    status = serializers.CharField(source="get_status_display")

    class Meta:
        """ MetaClass with model and fields"""
        model = EventStatus
        fields = ["status"]


class EventSerializer(serializers.ModelSerializer):
    """
    Event serializer
    """

    support_contact_id = serializers.ReadOnlyField(source="support_contact.id")
    client_id = serializers.ReadOnlyField(source="client.id")
    event_status_id = serializers.ReadOnlyField(source="event_status.id")
    event_status = EventStatusSerializer(many=False, read_only=True)

    class Meta:
        """ MetaClass with model and fields"""
        model = Event
        fields = [
            "id",
            "client_id",
            "support_contact_id",
            "event_status_id",
            "event_status",
            "attendees",
            "event_date",
            "notes",
            "date_created",
            "date_updated",
        ]

    def validate(self, data):
        """
        Method to validate the data to serialize
        """
        if (
            "support_contact_id" not in self._kwargs["data"]
            or "client_id" not in self._kwargs["data"]
        ):
            raise serializers.ValidationError(
                detail="support_contact_id and client_id are required in data",
                code="invalid",
            )
        return data

    def save(self, **kwargs):
        """
        Method to save the instance of Event
        """
        the_support_contact = get_object_or_404(
            SupportContact, pk=self._kwargs["data"]["support_contact_id"]
        )
        the_client = get_object_or_404(Client,
                                       pk=self._kwargs["data"]["client_id"])
        the_event_status = get_object_or_404(
            EventStatus, pk=self._kwargs["data"]["event_status_id"]
        )
        return super().save(
            support_contact=the_support_contact,
            client=the_client,
            event_status=the_event_status,
        )
