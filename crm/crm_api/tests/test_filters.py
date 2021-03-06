"""
Module test_filters.py
"""

import pytest
from crm_api.filters import ClientFilter, ContractFilter, EventFilter
from crm_api.models import Client, Contract, Event
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from parameterized import parameterized
from rest_framework.exceptions import PermissionDenied


class ClientFilterTest(TestCase):
    """
    TestCase for testing ClientFilter
    """

    fixtures = [
        "contenttype.json",
        "group.json",
        "permission.json",
        "user.json",
        "salescontact.json",
        "staffcontact.json",
        "supportcontact.json",
        "client.json",
        "eventstatus.json",
        "event.json",
    ]

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand(
        [
            ("yannis", 2),
            ("staff_contact_01", 2),
            ("staff_contact_filters_01", 2),
            ("sales_contact_01", 1),
            ("sales_contact_filters_01", 1),
            ("support_contact_01", 1),
            ("support_contact_filters_01", 1),
            ("anonymous_user", 0),
        ]
    )
    def test_filter(self, username, expected_items):
        """
        Test method filter_queryset of ClientFilter
        """
        factory = RequestFactory()
        request = factory.get("/")
        request.user = User.objects.get(username=username)
        if expected_items == 0:
            with self.assertRaises(PermissionDenied):
                ClientFilter().filter_queryset(
                    request=request, queryset=Client.objects.all()
                )
        else:
            client_filter_qs = ClientFilter().filter_queryset(
                request=request, queryset=Client.objects.all()
            )
            self.assertEqual(len(client_filter_qs), expected_items)


class ContractFilterTest(TestCase):
    """
    TestCase for testing ContractFilter
    """

    fixtures = [
        "contenttype.json",
        "group.json",
        "permission.json",
        "user.json",
        "salescontact.json",
        "staffcontact.json",
        "supportcontact.json",
        "client.json",
        "contract.json",
        "eventstatus.json",
        "event.json",
    ]

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand(
        [
            ("yannis", 3),
            ("staff_contact_01", 3),
            ("staff_contact_filters_01", 3),
            ("sales_contact_01", 2),
            ("sales_contact_filters_01", 2),
            ("support_contact_01", 0),
            ("support_contact_filters_01", 0),
            ("anonymous_user", 0),
        ]
    )
    def test_filter(self, username, expected_items):
        """
        Test method filter_queryset of ContractFilter
        """
        factory = RequestFactory()
        request = factory.get("/")
        request.user = User.objects.get(username=username)
        if expected_items == 0:
            with self.assertRaises(PermissionDenied):
                ContractFilter().filter_queryset(
                    request=request, queryset=Contract.objects.all()
                )
        else:
            contract_filter_qs = ContractFilter().filter_queryset(
                request=request, queryset=Contract.objects.all()
            )
            self.assertEqual(len(contract_filter_qs), expected_items)


class EventFilterTest(TestCase):
    """
    TestCase for testing EventFilter
    """

    fixtures = [
        "contenttype.json",
        "group.json",
        "permission.json",
        "user.json",
        "salescontact.json",
        "staffcontact.json",
        "supportcontact.json",
        "client.json",
        "contract.json",
        "eventstatus.json",
        "event.json",
    ]

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand(
        [
            ("yannis", 2),
            ("staff_contact_01", 2),
            ("staff_contact_filters_01", 2),
            ("sales_contact_01", 1),
            ("sales_contact_filters_01", 2),
            ("support_contact_01", 1),
            ("support_contact_filters_01", 1),
            ("anonymous_user", 0),
        ]
    )
    def test_filter(self, username, expected_items):
        """
        Test method filter_queryset of EventFilter
        """
        factory = RequestFactory()
        request = factory.get("/")
        request.user = User.objects.get(username=username)
        if expected_items == 0:
            with self.assertRaises(PermissionDenied):
                EventFilter().filter_queryset(
                    request=request, queryset=Event.objects.all()
                )
        else:
            event_filter_qs = EventFilter().filter_queryset(
                request=request, queryset=Event.objects.all()
            )
            self.assertEqual(len(event_filter_qs), expected_items)
