from datetime import timedelta

import factory
from django.utils import timezone

from django.contrib.auth.models import User

from crm_api.models import (Client, Contract, Event, EventStatus, SalesContact,
                            StaffContact, SupportContact)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = "testuser"
    password = "testuser"


class SalesContactFactory(factory.Factory):
    class Meta:
        model = SalesContact


    user = User(username="testsalescontact", password="test")
    user_id = user.id


class SupportContactFactory(factory.Factory):
    class Meta:
        model = SupportContact

    user = User(username="testsupportcontact", password="test")
    user_id = user.id


class StaffContactFactory(factory.Factory):
    class Meta:
        model = StaffContact

    user = User(username="teststaffcontact", password="test")
    user_id = user.id


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    first_name = "Test"
    last_name = "Client"
    email = "testclient@testbase.com"
    phone = "123456789"
    mobile = ""
    sales_contact = factory.SubFactory(SalesContactFactory)
    sales_contact_id = id(sales_contact)


class ContractFactory(factory.Factory):
    class Meta:
        model = Contract

    status = True
    amount = 9157863.25
    payment_due = timezone.now() + timedelta(days=30)
    client = factory.SubFactory(ClientFactory)
    client_id = id(client)
    sales_contact = factory.SubFactory(SalesContactFactory)
    sales_contact_id = id(sales_contact)


class EventStatusFactory(factory.Factory):
    class Meta:
        model = EventStatus

    status = EventStatus.Status.CREATED


class EventFactory(factory.Factory):
    class Meta:
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
