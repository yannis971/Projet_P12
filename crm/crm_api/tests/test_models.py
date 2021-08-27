import mock
import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User, Group
from crm_api.models import Client, Contract, EventStatus, Event, SalesContact, StaffContact, SupportContact


class SalesContactModelTest(TestCase):

    def setUp(self):
        self.user = User(username="TESTSALESCONTACT", password="test")
        self.contact = SalesContact(user=self.user)

    def test_create(self):
        assert isinstance(self.contact, SalesContact)

    def test_str(self):
        assert self.contact.__str__() == "TESTSALESCONTACT"


class SupportContactModelTest(TestCase):

    def setUp(self):
        self.user = User(username="TESTSUPPORTCONTACT", password="test")
        self.contact = SupportContact(user=self.user)

    def test_create(self):
        assert isinstance(self.contact, SupportContact)

    def test_str(self):
        assert self.contact.__str__() == "TESTSUPPORTCONTACT"


class StaffContactModelTest(TestCase):

    def setUp(self):
        self.user = User(username="TESTSTAFFCONTACT", password="test")
        self.contact = StaffContact(user=self.user)

    def test_create(self):
        assert isinstance(self.contact, StaffContact)

    def test_str(self):
        assert self.contact.__str__() == "TESTSTAFFCONTACT"


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
        sales_contact = SalesContact.objects.create(user=User(username="test_sales_contact", password="test"))
        client = Client.objects.create(first_name="test", last_name="client", email="testclient@example.com", sales_contact=sales_contact)
        Contract.objects.create(sales_contact=sales_contact, client=client, status=True, amount=1000.00,
                                payment_due=datetime.fromisoformat('2021-12-01 00:00:00.000+00:00'))

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_create_contract(self):
        contract = Contract.objects.get(id=1)
        assert isinstance(contract, Contract)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_contract_str(self):
        contract = Contract.objects.get(id=1)
        assert contract.__str__() == "test client | test_sales_contact | True | 1000.00 | 2021-12-01 00:00:00+00:00"

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
        sales_contact = SalesContact.objects.create(user=User(username="test_sales_contact", password="test"))
        client = Client.objects.create(first_name="test", last_name="client", email="testclient@example.com", sales_contact=sales_contact)
        support_contact = SupportContact.objects.create(user=User(username="test_support_contact", password="test"))
        Event.objects.create(support_contact=support_contact, client=client, event_status=EventStatus.objects.get(status="C"), attendees=100,
                            notes="Test Event Model",
                            event_date=datetime.fromisoformat('2021-12-01 00:00:00.000+00:00'))

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_create_event(self):
        event = Event.objects.get(id=1)
        assert isinstance(event, Event)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_event_str(self):
        event = Event.objects.get(id=1)
        assert event.__str__() == "test client | test_support_contact | CREATED | 100 | 2021-12-01 00:00:00+00:00"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_event_count(self):
        assert Event.objects.count() == 1
