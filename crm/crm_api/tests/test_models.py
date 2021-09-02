from datetime import datetime

import mock
import pytest
from crm_api.models import (Client, Contract, Event, EventStatus, SalesContact,
                            StaffContact, SupportContact)
from django.contrib.auth.models import User, Group
from django.test import TestCase


class SalesContactModelTest(TestCase):
    @classmethod
    @pytest.mark.django_db
    def setUpTestData(cls):
        Group.objects.create(name="SALES")
        SalesContact.objects.create(
            user=User(username="test_sales_contact", password="test")
        )

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_create(self):
        sales_contact = SalesContact.objects.get(pk=1)
        assert isinstance(sales_contact, SalesContact)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_str(self):
        sales_contact = SalesContact.objects.get(pk=1)
        assert sales_contact.__str__() == "test_sales_contact"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_group(self):
        sales_contact = SalesContact.objects.get(pk=1)
        assert sales_contact.user.groups.all()[0].name == "SALES"


class SupportContactModelTest(TestCase):
    @classmethod
    @pytest.mark.django_db
    def setUpTestData(cls):
        Group.objects.create(name="SUPPORT")
        SupportContact.objects.create(
            user=User(username="test_support_contact", password="test")
        )

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_create(self):
        support_contact = SupportContact.objects.get(pk=1)
        assert isinstance(support_contact, SupportContact)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_str(self):
        support_contact = SupportContact.objects.get(pk=1)
        assert support_contact.__str__() == "test_support_contact"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_group(self):
        support_contact = SupportContact.objects.get(pk=1)
        assert support_contact.user.groups.all()[0].name == "SUPPORT"


class StaffContactModelTest(TestCase):
    @classmethod
    @pytest.mark.django_db
    def setUpTestData(cls):
        Group.objects.create(name="STAFF")
        StaffContact.objects.create(
            user=User(username="test_staff_contact", password="test")
        )

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_create(self):
        staff_contact = StaffContact.objects.get(pk=1)
        assert isinstance(staff_contact, StaffContact)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_str(self):
        staff_contact = StaffContact.objects.get(pk=1)
        assert staff_contact.__str__() == "test_staff_contact"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_group(self):
        staff_contact = StaffContact.objects.get(pk=1)
        assert staff_contact.user.groups.all()[0].name == "STAFF"


class ClientModelTest(TestCase):
    def setUp(self):
        sales_contact = mock.Mock(spec=SalesContact)
        sales_contact._state = mock.Mock()
        sales_contact.username = "test"
        self.test_client = Client()
        self.test_client.first_name = "Test"
        self.test_client.last_name = "Client"
        self.test_client.email = "testclient@testbase.com"
        self.test_client.sales_contact = sales_contact

    def test_create_client(self):
        assert isinstance(self.test_client, Client)

    def test_client_sales_contact(self):
        assert isinstance(self.test_client.sales_contact, SalesContact)

    def test_client_str(self):
        assert self.test_client.__str__() == "Test Client"


class ContractModelTest(TestCase):
    @classmethod
    @pytest.mark.django_db
    def setUpTestData(cls):
        Group.objects.create(name="SALES")
        sales_contact = SalesContact.objects.create(
            user=User(username="test_sales_contact", password="test")
        )
        client = Client.objects.create(
            first_name="test",
            last_name="client",
            email="testclient@example.com",
            sales_contact=sales_contact,
        )
        date_iso = "2021-12-01 00:00:00.000+00:00"
        Contract.objects.create(
            sales_contact=sales_contact,
            client=client,
            status=True,
            amount=1000.00,
            payment_due=datetime.fromisoformat(date_iso),
        )

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_create_contract(self):
        contract = Contract.objects.get(pk=1)
        assert isinstance(contract, Contract)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_contract_str(self):
        contract = Contract.objects.get(pk=1)
        expected_str_01 = "test client | test_sales_contact | True | 1000.00 |"
        expected_str_02 = " 2021-12-01 00:00:00+00:00"
        assert (
            contract.__str__()
            == expected_str_01 + expected_str_02
        )

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_contract_count(self):
        assert Contract.objects.count() == 1


class EventStatusModelTest(TestCase):
    @classmethod
    @pytest.mark.django_db
    def setUpTestData(cls):
        for status in EventStatus.Status:
            EventStatus.objects.create(status=status)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_create_event_status(self):
        for item in EventStatus.objects.all():
            assert isinstance(item, EventStatus)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_event_status_count(self):
        assert EventStatus.objects.count() == len(EventStatus.Status)


class EventModelTest(TestCase):
    @classmethod
    @pytest.mark.django_db
    def setUpTestData(cls):
        Group.objects.create(name="SALES")
        Group.objects.create(name="SUPPORT")
        EventStatus.objects.create(status="C")
        sales_contact = SalesContact.objects.create(
            user=User(username="test_sales_contact", password="test")
        )
        client = Client.objects.create(
            first_name="test",
            last_name="client",
            email="testclient@example.com",
            sales_contact=sales_contact,
        )
        support_contact = SupportContact.objects.create(
            user=User(username="test_support_contact", password="test")
        )
        Event.objects.create(
            support_contact=support_contact,
            client=client,
            event_status=EventStatus.objects.get(status="C"),
            attendees=100,
            notes="Test Event Model",
            event_date=datetime.fromisoformat("2021-12-01 00:00:00.000+00:00"),
        )

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_create_event(self):
        event = Event.objects.get(pk=1)
        assert isinstance(event, Event)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_event_str(self):
        event = Event.objects.get(pk=1)
        expected_str_01 = "test client | test_support_contact | CREATED |"
        expected_str_02 = " 100 | 2021-12-01 00:00:00+00:00"
        assert (
            event.__str__()
            == expected_str_01 + expected_str_02
        )

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_event_count(self):
        assert Event.objects.count() == 1
