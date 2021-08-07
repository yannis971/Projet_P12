import pytest
from datetime import datetime
from django.test import TestCase
from crm_api.models import Client, SalesContact, Contract

class SalesContactModelTest(TestCase):
    def setUp(self):
        self.username = "testsalescontact"
        self.email = "testsalescontact@testbase.com"
        self.first_name = "Test"
        self.last_name = "SalesContact"
        self.password = "test"

        self.test_user = SalesContact.objects.create_user(
            username=self.username,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password
        )
        return self.test_user

    def test_create_user(self):
        assert isinstance(self.test_user, SalesContact)

    def test_default_user_is_active(self):
        assert self.test_user.is_active

    def test_default_user_is_staff(self):
        assert not self.test_user.is_staff

    def test_default_user_is_superuser(self):
        assert not self.test_user.is_superuser

    def test_get_full_name(self):
        assert self.test_user.get_full_name() == 'Test SalesContact'

    def test_get_short_name(self):
        assert self.test_user.get_short_name() == self.first_name

    def test_get_username(self):
        assert self.test_user.get_username() == self.username

    def test_user_count(self):
        assert SalesContact.objects.count() == 1


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
        self.payment_due = datetime(2024, 12, 31, 23, 59, 59, 0)
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
