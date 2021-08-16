import mock
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from crm_api.models import Client, Contract, EventStatus, Event, SalesContact, StaffContact, SupportContact, User


class UserModelTest:

    def __init__(self):
        self.username = "testuser"
        self.email = "user@testbase.com"
        self.first_name = "Test"
        self.last_name = "User"
        self.password = "test"
        self.model = User
        self.test_user = self.model.objects.create_user(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )

    def test_create_user(self):
        assert isinstance(self.test_user, self.model)

    def test_default_user_is_active(self):
        assert self.test_user.is_active

    def test_default_user_is_staff(self):
        assert not self.test_user.is_staff

    def test_default_user_is_superuser(self):
        assert not self.test_user.is_superuser

    def test_get_full_name(self):
        assert self.test_user.get_full_name() == f"{self.first_name} {self.last_name}"

    def test_get_short_name(self):
        assert self.test_user.get_short_name() == self.first_name

    def test_get_username(self):
        assert self.test_user.get_username() == self.username

    def test_user_count(self):
        assert self.model.objects.count() == 1


class SalesContactModelTest(TestCase, UserModelTest):

    def setUp(self):
        self.username = "testsalescontact"
        self.email = "testsalescontact@testbase.com"
        self.first_name = "Test"
        self.last_name = "SalesContact"
        self.password = "test"

        self.model = SalesContact

        self.test_user = self.model.objects.create_user(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )
        return self.test_user


class SupportContactModelTest(TestCase, UserModelTest):

    def setUp(self):
        self.username = "testsupportcontact"
        self.email = "testsupportcontact@testbase.com"
        self.first_name = "Test"
        self.last_name = "SupportContact"
        self.password = "test"

        self.model = SupportContact

        self.test_user = self.model.objects.create_user(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )
        return self.test_user


class StaffContactModelTest(TestCase, UserModelTest):

    def setUp(self):
        self.username = "teststaffcontact"
        self.email = "teststaffcontact@testbase.com"
        self.first_name = "Test"
        self.last_name = "StaffContact"
        self.password = "test"

        self.model = StaffContact

        self.test_user = self.model.objects.create_user(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )
        return self.test_user


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

    def setUp(self):
        client = mock.Mock(spec=Client)
        client._state = mock.Mock()
        client.first_name = "test"
        sales_contact = mock.Mock(spec=SalesContact)
        sales_contact._state = mock.Mock()
        sales_contact.username = "salescontact"
        self.test_contract = Contract()
        self.test_contract.status = True
        self.test_contract.amount = 15786.25
        self.test_contract.payment_due = timezone.now() + timedelta(days=30)
        self.test_contract.client = client
        # self.test_contract.sales_contact = client.sales_contact

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
        self.test_event = Event()
        self.test_event.attendees = 100
        self.test_event.event_date = timezone.now() + timedelta(days=15)
        self.test_event.notes = "Test Event Model"
        client = mock.Mock(spec=Client)
        client._state = mock.Mock()
        client.first_name = "test"
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


