import pytest
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from crm_api.models import SalesContact, SupportContact, StaffContact, User, Client

from parameterized import parameterized

"""
@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

@pytest.mark.django_db
def test_create_users():
    Group.objects.create(name="STAFF")
    Group.objects.create(name="SALES")
    Group.objects.create(name="SUPPORT")
    SalesContact.objects.create(user=User(username="test_sales_contact", password="test"))
    StaffContact.objects.create(user=User(username="test_staff_contact", password="test"))
    SupportContact.objects.create(user=User(username="test_support_contact", password="test"))
    assert Group.objects.count() == 3
    assert User.objects.count() == 3


@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, password, status_code', [
        (None, None, 400),
        (None, 'password', status.HTTP_400_BAD_REQUEST),
        ('username', None, status.HTTP_400_BAD_REQUEST),
        ('test_sales_contact', 'invalid_password', status.HTTP_403_FORBIDDEN),
        ('test_sales_contact', 'test', status.HTTP_200_OK),
    ]
)
def test_login(username, password, status_code, api_client):
    #url = reverse('login')
    url = '/login/'
    data = {'username': username, 'password': password}
    response = api_client.post(url, data, format='json')
    if status_code == status.HTTP_200_OK:
        print("User.objects.count() :", User.objects.count())
    assert response.status_code == status_code

"""


class LoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user
        User.objects.create_user(
            username='test_user',
            password='test',
        )

    @pytest.mark.django_db
    @parameterized.expand([
        ('', '', status.HTTP_400_BAD_REQUEST),
        ('', 'password', status.HTTP_400_BAD_REQUEST),
        ('username', '', status.HTTP_400_BAD_REQUEST),
        ('test_user', 'invalid_password', status.HTTP_403_FORBIDDEN),
        ('test_user', 'test', status.HTTP_200_OK),
    ])
    def test_login(self, username, password, status_code):
        url = '/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            self.assertIn('token', response.data)

    def test_get_method(self):
        url = '/login/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @parameterized.expand([
        ("DELETE",),
        ("PATCH", ),
        ("PUT",),
    ])
    def test_method_not_allowed(self, method):
        url = '/login/'
        if method == "DELETE":
            response = self.client.delete(url)
        elif method == "PUT":
            response = self.client.put(url)
        else:
            response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class LogoutViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user
        User.objects.create_user(
            username='test_user',
            password='test',
        )

    def test_login_logout(self):
        url = '/login/'
        data = {'username': 'test_user', 'password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = '/logout/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Your are now logged out")


class SalesContactViewTest(TestCase):

    fixtures = ['contenttype.json', 'group.json', 'permission.json']

    @classmethod
    def setUpTestData(cls):
        # Create users
        User.objects.create_user(
            username='sales_contact',
            password='test',
        )
        SalesContact.objects.create(user=User.objects.get(username='sales_contact'))
        User.objects.create_user(
            username='support_contact',
            password='test',
        )
        SupportContact.objects.create(user=User.objects.get(username='support_contact'))
        User.objects.create_user(
            username='staff_contact',
            password='test',
        )
        StaffContact.objects.create(user=User.objects.get(username='staff_contact'))
        User.objects.create_user(
            username='anonymous_user',
            password='test',
        )

    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', status.HTTP_403_FORBIDDEN),
        ('support_contact', 'test', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', status.HTTP_200_OK),
        ('anonymous_user', 'test', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_salescontact(self, username, password, status_code):
        url = '/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = '/salescontacts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)


class ClientViewTest(TestCase):

    fixtures = ['contenttype.json', 'group.json', 'permission.json']

    @classmethod
    def setUpTestData(cls):
        # Create users
        User.objects.create_user(
            username='sales_contact',
            password='test',
        )
        sales_contact = SalesContact.objects.create(user=User.objects.get(username='sales_contact'))
        Client.objects.create(first_name="first",
                              last_name="client",
                              email="first.client@example.com",
                              sales_contact=sales_contact)
        User.objects.create_user(
            username='support_contact',
            password='test',
        )
        SupportContact.objects.create(user=User.objects.get(username='support_contact'))
        User.objects.create_user(
            username='staff_contact',
            password='test',
        )
        StaffContact.objects.create(user=User.objects.get(username='staff_contact'))
        User.objects.create_user(
            username='anonymous_user',
            password='test',
        )

    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', status.HTTP_200_OK),
        ('support_contact', 'test', status.HTTP_200_OK),
        ('staff_contact', 'test', status.HTTP_200_OK),
        ('anonymous_user', 'test', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_client(self, username, password, status_code):
        url = '/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = '/clients/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', status.HTTP_201_CREATED),
        ('support_contact', 'test', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', status.HTTP_403_FORBIDDEN),
        ('anonymous_user', 'test', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_client(self, username, password, status_code):
        url = '/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = '/clients/'
        if username == 'sales_contact':
            user = User.objects.get(username='sales_contact')
            sales_contact = SalesContact.objects.get(user=user)
            data = {'first_name': 'second',
                    'last_name': 'client',
                    'email': 'second.client@example.com',
                    'phone': '',
                    'mobile': '',
                    'sales_contact_id': sales_contact.sales_contact_id}
        else:
            data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', '33489916502', '33786753421', status.HTTP_200_OK),
        ('support_contact', 'test', '', '', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', '33145913572', '33646258429', status.HTTP_200_OK),
        ('anonymous_user', 'test', '', '', status.HTTP_403_FORBIDDEN),
    ])
    def test_change_client(self, username, password, phone, mobile, status_code):
        url = '/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = '/clients/1/'
        if username == 'sales_contact' or username == 'staff_contact':
            user = User.objects.get(username='sales_contact')
            sales_contact = SalesContact.objects.get(user=user)
            data = {'first_name': 'second',
                    'last_name': 'client',
                    'email': 'second.client@example.com',
                    'phone': phone,
                    'mobile': mobile,
                    'sales_contact_id': sales_contact.sales_contact_id}
            print(username, "data :", data)
        else:
            data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['phone'], new_phone)
            self.assertEqual(response.data['mobile'], new_mobile)

