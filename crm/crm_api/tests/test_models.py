import pytest
from django.test import TestCase
from crm_api.models import Client, SalesContact

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
        assert self.test_user.get_short_name() == self.email

    @pytest.mark.django_db
    def test_user_count():
        assert SalesContact.objects.count() == 1
