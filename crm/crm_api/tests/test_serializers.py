"""
Module test_serializers.py
"""
from datetime import timedelta

import factory
import pytest
from crm_api.factories import (ClientFactory, ContractFactory, EventFactory,
                               SalesContactFactory, StaffContactFactory,
                               SupportContactFactory, UserFactory)
from crm_api.serializers import (ClientSerializer, ContractSerializer,
                                 EventSerializer, SalesContactSerializer,
                                 StaffContactSerializer,
                                 SupportContactSerializer, UserSerializer)
from django.test import TestCase
from django.utils import timezone


class TestClientSerializer(TestCase):
    """
    TestCase for testing ClientSerializer
    """
    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        client = ClientFactory.build()
        serializer = ClientSerializer(client)

        assert serializer.data

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialized_data(self):
        valid_serialized_data = factory.build(
            dict, FACTORY_CLASS=ClientFactory
        )
        serializer = ClientSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_max_length_error(self):
        non_valid_data = {
            "first_name": "x" * 26,
            "last_name": "y" * 26,
            "email": "testclient@testbase.com" * 10,
            "phone": "9" * 21,
            "mobile": "6" * 21,
        }
        serializer = ClientSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        for key in non_valid_data.keys():
            assert serializer.errors[key][0].code == "max_length"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_blank_value_error(self):
        non_valid_data = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "phone": "",
            "mobile": "",
        }
        serializer = ClientSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        for key in "first_name", "last_name", "email":
            assert serializer.errors[key][0].code == "blank"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_email_error(self):
        non_valid_data = {
            "first_name": "Test",
            "last_name": "Client",
            "email": "testclientxtestbase.com",
            "phone": "123456789",
            "mobile": "",
        }
        serializer = ClientSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        assert serializer.errors["email"][0].code == "invalid"


class TestContractSerializer(TestCase):
    """
    TestCase for testing ContractSerializer
    """
    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        contract = ContractFactory.build()
        serializer = ContractSerializer(contract)

        assert serializer.data

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialized_data(self):
        valid_serialized_data = factory.build(
            dict,
            FACTORY_CLASS=ContractFactory
        )
        serializer = ContractSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_status_error(self):
        non_valid_data = {
            "status": "string",
            "amount": 9157863.25,
            "payment_due": timezone.now() + timedelta(days=30),
        }
        serializer = ContractSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        assert serializer.errors["status"][0].code == "invalid"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_amount_max_digits_error(self):
        non_valid_data = {
            "status": False,
            "amount": 49157863.25,
            "payment_due": timezone.now() + timedelta(days=30),
        }
        serializer = ContractSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        assert serializer.errors["amount"][0].code == "max_digits"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_amount_type_error(self):
        non_valid_data = {
            "status": False,
            "amount": "string",
            "payment_due": timezone.now() + timedelta(days=30),
        }
        serializer = ContractSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        assert serializer.errors["amount"][0].code == "invalid"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_payment_due_error(self):
        non_valid_data = {
            "status": False,
            "amount": 9157863.25,
            "payment_due": "2020-12-31",
        }
        serializer = ContractSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        assert serializer.errors["payment_due"][0].code == "invalid"


class TestEventSerializer(TestCase):
    """
    TestCase for testing EventSerializer
    """
    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        event = EventFactory.build()
        serializer = EventSerializer(event)

        assert serializer.data

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialized_data(self):
        valid_serialized_data = factory.build(dict, FACTORY_CLASS=EventFactory)
        serializer = EventSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_attendees_type_error(self):
        non_valid_data = {
            "attendees": False,
            "event_date": timezone.now() + timedelta(days=30),
            "notes": "Test Event Model",
        }
        serializer = EventSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        assert serializer.errors["attendees"][0].code == "invalid"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_event_date_error(self):
        non_valid_data = {
            "attendees": 100,
            "event_date": "2021-12-31",
            "notes": "Test Event Model",
        }
        serializer = EventSerializer(data=non_valid_data)

        self.assertIsNot(serializer.is_valid(), True)
        assert serializer.errors["event_date"][0].code == "invalid"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_notes_type_error(self):
        non_valid_data = {
            "attendees": 100,
            "event_date": timezone.now() + timedelta(days=30),
            "notes": [1, 2, 3, 4],
        }
        serializer = EventSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        assert serializer.errors["notes"][0].code == "invalid"

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_notes_max_length_error(self):
        non_valid_data = {
            "attendees": 100,
            "event_date": timezone.now() + timedelta(days=30),
            "notes": "x" * 2049,
        }
        serializer = EventSerializer(data=non_valid_data)

        self.assertFalse(serializer.is_valid())
        assert serializer.errors["notes"][0].code == "max_length"


class TestUserSerializer(TestCase):
    """
    TestCase for testing UserSerializer
    """
    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        user = UserFactory.build()
        serializer = UserSerializer(user)

        assert serializer.data

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialized_data(self):
        valid_serialized_data = factory.build(dict, FACTORY_CLASS=UserFactory)
        serializer = UserSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}


class TestSalesContactSerializer:
    """
    TestCase for testing SalesContactSerializer
    """
    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        sales_contact = SalesContactFactory.build()
        serializer = SalesContactSerializer(sales_contact)

        assert serializer.data

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialized_data(self):
        valid_serialized_data = {
            "user": {
                "username": "testsalescontact",
                "password": "test",
                "groups": [
                    {"name": "SALES"},
                ],
            }
        }
        serializer = SalesContactSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}


class TestSupportContactSerializer(TestCase):
    """
    TestCase for testing SupportContactSerializer
    """
    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        support_contact = SupportContactFactory.build()
        serializer = SupportContactSerializer(support_contact)

        assert serializer.data

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialized_data(self):
        valid_serialized_data = {
            "user": {
                "username": "testsupportcontact",
                "password": "test",
                "groups": [
                    {"name": "SUPPORT"},
                ],
            }
        }
        serializer = SupportContactSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}


class TestStaffContactSerializer(TestCase):
    """
    TestCase for testing StaffContactSerializer
    """
    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialize_model(self):
        staff_contact = StaffContactFactory.build()
        serializer = StaffContactSerializer(staff_contact)

        self.assert_(serializer.data)

    @pytest.mark.unit
    @pytest.mark.django_db
    def test_serialized_data(self):
        valid_serialized_data = {
            "user": {
                "username": "teststaffcontact",
                "password": "test",
                "groups": [
                    {"name": "SUPPORT"},
                ],
            }
        }
        serializer = StaffContactSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}
