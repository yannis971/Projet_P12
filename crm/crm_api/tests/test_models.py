import mock
import pytest
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
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
    @pytest.mark.unit
    @pytest.mark.django_db
    def setUp(self):
        sales_contact = mock.Mock(spec=SalesContact)
        sales_contact.username = "salescontact"
        sales_contact._state = mock.Mock(name="sales_contact")
        client = mock.Mock(spec=Client)
        client._state = mock.Mock(name="client")
        client.first_name = "test"
        client.sales_contact = sales_contact
        self.test_contract = Contract()
        self.test_contract.status = True
        self.test_contract.amount = 15786.25
        self.test_contract.payment_due = timezone.now() + timedelta(days=30)
        self.test_contract.client = client
        # self.test_contract.sales_contact = sales_contact


    @pytest.mark.unit
    @pytest.mark.django_db
    def test_create_contract(self):
        assert isinstance(self.test_contract, Contract)


class EventStatusModelTest(TestCase):

    def setUp(self):
        self.test_event_status = []
        for status in EventStatus.Status:
            self.test_event_status.append(EventStatus.objects.create(status=status))
        return self.test_event_status

    def test_create_event_status(self):
        for item in self.test_event_status:
            assert isinstance(item, EventStatus)

    def test_event_status_count(self):
        assert EventStatus.objects.count() == len(EventStatus.Status)


class EventModelTest(TestCase):

    def setUp(self):
        client = mock.Mock(spec=Client)
        client._state = mock.Mock(name="client")
        client.first_name = "test"
        self.test_event = Event()
        self.test_event.attendees = 100
        self.test_event.event_date = timezone.now() + timedelta(days=15)
        self.test_event.notes = "Test Event Model"
        self.test_event.client = client
        """
        support_contact = mock.Mock(spec=SupportContact)
        support_contact._state = mock.Mock()
        support_contact.username = "supportcontact"
        self.test_event.support_contact = support_contact
        event_status = mock.Mock(spec=EventStatus)
        event_status._state = mock.Mock()
        self.test_event.event_status = event_status
        """

    def test_create_event(self):
        assert isinstance(self.test_event, Event)
