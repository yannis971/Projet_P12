import pytest
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
        self.first_name = "Test"
        self.last_name = "Client"
        self.email = "testclient@testbase.com"
        self.phone = ""
        self.mobile = ""
        self.sales_contact = SalesContactModelTest().setUp()
        self.test_client = Client.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            mobile=self.mobile,
            sales_contact=self.sales_contact
        )
        return self.test_client

    def test_create_client(self):
        assert isinstance(self.test_client, Client)

    def test_client_sales_contact(self):
        assert isinstance(self.test_client.sales_contact, SalesContact)

    def test_client_str(self):
        assert self.test_client.__str__() == f"{self.first_name} {self.last_name}"

    def test_client_count(self):
        assert Client.objects.count() == 1


class ContractModelTest(TestCase):

    def setUp(self):
        self.status = True
        self.amount = 15786.25
        self.payment_due = timezone.now() + timedelta(days=30)
        self.client = ClientModelTest().setUp()
        self.sales_contact = self.client.sales_contact
        self.test_contract = Contract.objects.create(
            sales_contact=self.sales_contact,
            client=self.client,
            status=self.status,
            amount=self.amount,
            payment_due=self.payment_due
        )

    def test_create_contract(self):
        assert isinstance(self.test_contract, Contract)

    def test_contract_count(self):
        assert Contract.objects.count() == 1


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
        self.client = ClientModelTest().setUp()
        self.support_contact = SupportContactModelTest().setUp()
        self.event_status = EventStatusModelTest().setUp()[0]
        self.attendees = 100
        self.event_date = timezone.now() + timedelta(days=15)
        self.notes = "Test Event Model"
        self.test_event = Event.objects.create(
            client=self.client,
            support_contact=self.support_contact,
            event_status=self.event_status,
            attendees=self.attendees,
            event_date=self.event_date,
            notes=self.notes
        )

    def test_create_event(self):
        assert isinstance(self.test_event, Event)

    def test_event_count(self):
        assert Event.objects.count() == 1
