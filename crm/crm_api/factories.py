"""
Module factories
"""
from datetime import timedelta

import factory
from django.contrib.auth.models import User
from django.utils import timezone

from crm_api.models import (
    Client,
    Contract,
    Event,
    EventStatus,
    SalesContact,
    StaffContact,
    SupportContact,
)


class UserFactory(factory.Factory):
    """
    class UserFactory
    """
    class Meta:
        """ MetaClass with model"""
        model = User

    username = "testuser"
    password = "testuser"


class SalesContactFactory(factory.Factory):
    """
    class SalesContactFactory
    """
    class Meta:
        """ MetaClass with model"""
        model = SalesContact

    user = User(username="testsalescontact", password="test")


class SupportContactFactory(factory.Factory):
    """
    class SupportContactFactory
    """
    class Meta:
        """ MetaClass with model"""
        model = SupportContact

    user = User(username="testsupportcontact", password="test")


class StaffContactFactory(factory.Factory):
    """
    class StaffContactFactory
    """
    class Meta:
        """ MetaClass with model"""
        model = StaffContact

    user = User(username="teststaffcontact", password="test")


class ClientFactory(factory.Factory):
    """
    class ClientFactory
    """
    class Meta:
        """ MetaClass with model"""
        model = Client

    first_name = "Test"
    last_name = "Client"
    email = "testclient@testbase.com"
    phone = "123456789"
    mobile = ""
    sales_contact = factory.SubFactory(SalesContactFactory)
    sales_contact_id = id(sales_contact)


class ContractFactory(factory.Factory):
    """
    class ContractFactory
    """
    class Meta:
        """ MetaClass with model"""
        model = Contract

    status = True
    amount = 9157863.25
    payment_due = timezone.now() + timedelta(days=30)
    client = factory.SubFactory(ClientFactory)
    client_id = id(client)
    sales_contact = factory.SubFactory(SalesContactFactory)
    sales_contact_id = id(sales_contact)


class EventStatusFactory(factory.Factory):
    """
    class EventStatusFactory
    """
    class Meta:
        """ MetaClass with model"""
        model = EventStatus

    status = EventStatus.Status.CREATED


class EventFactory(factory.Factory):
    """
    class EventFactory
    """
    class Meta:
        """ MetaClass with model"""
        model = Event

    client = factory.SubFactory(ClientFactory)
    client_id = id(client)
    support_contact = factory.SubFactory(SupportContactFactory)
    support_contact_id = id(support_contact)
    event_status = factory.SubFactory(EventStatusFactory)
    event_status_id = id(event_status)
    attendees = 100
    event_date = timezone.now() + timedelta(days=15)
    notes = "Test Event Model"
