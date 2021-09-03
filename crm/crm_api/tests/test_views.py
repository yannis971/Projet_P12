import pytest

from datetime import datetime
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from crm_api.models import SalesContact, SupportContact, StaffContact, User, Client, Contract, EventStatus, Event
from crm_api.serializers import ContractSerializer, EventSerializer

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
        response = self.client.post(url, data, content_type='application/json')
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
        response = self.client.post(url, data, content_type='application/json')
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
        response = self.client.post(url, data, content_type='application/json')
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
    def login(self, username, password):
        url = '/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', status.HTTP_200_OK),
        ('support_contact', 'test', status.HTTP_200_OK),
        ('staff_contact', 'test', status.HTTP_200_OK),
        ('anonymous_user', 'test', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_client(self, username, password, status_code):
        self.login(username, password)
        url = '/clients/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(2)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', status.HTTP_201_CREATED),
        ('support_contact', 'test', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', status.HTTP_201_CREATED),
        ('anonymous_user', 'test', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_client(self, username, password, status_code):
        self.login(username, password)
        url = '/clients/'
        if username == 'sales_contact' or username == 'staff_contact':
            user = User.objects.get(username='sales_contact')
            sales_contact = SalesContact.objects.get(user=user)
            data = {'first_name': 'new client',
                    'last_name': f'by {username}',
                    'email': 'second.client@example.com',
                    'phone': '',
                    'mobile': '',
                    'sales_contact_id': sales_contact.id}
        else:
            data = {}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(3)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', '33489916502', '33786753421', status.HTTP_200_OK),
        ('support_contact', 'test', '', '', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', '33145913572', '33646258429', status.HTTP_200_OK),
        ('anonymous_user', 'test', '', '', status.HTTP_403_FORBIDDEN),
    ])
    def test_change_client(self, username, password, new_phone, new_mobile, status_code):
        self.login(username, password)
        url = '/clients/1/'
        if username == 'sales_contact' or username == 'staff_contact':
            user = User.objects.get(username='sales_contact')
            sales_contact = SalesContact.objects.get(user=user)
            data = {'first_name': 'second',
                    'last_name': 'client',
                    'email': 'second.client@example.com',
                    'phone': new_phone,
                    'mobile': new_mobile,
                    'sales_contact_id': sales_contact.id}
        else:
            data = {}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['phone'], new_phone)
            self.assertEqual(response.data['mobile'], new_mobile)

    @pytest.mark.order(4)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact', 'test', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', 1, status.HTTP_204_NO_CONTENT),
        ('anonymous_user', 'test', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_client(self, username, password, pk, status_code):
        self.login(username, password)
        url = f'/clients/{pk}/'
        response = self.client.delete(url, data='', content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_204_NO_CONTENT:
            self.assertEqual(Client.objects.count(), 0)
        else:
            self.assertEqual(Client.objects.count(), 1)


class ContractViewTest(TestCase):
    fixtures = ['contenttype.json', 'group.json', 'permission.json']

    @classmethod
    def setUpTestData(cls):
        # Create users
        User.objects.create_user(
            username='sales_contact',
            password='test',
        )
        sales_contact = SalesContact.objects.create(user=User.objects.get(username='sales_contact'))
        client = Client.objects.create(first_name="first_name",
                                       last_name="last_name",
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
        date_iso = "2021-12-01 00:00:00.000+00:00"
        Contract.objects.create(
            sales_contact=sales_contact,
            client=client,
            status=True,
            amount=1000.00,
            payment_due=datetime.fromisoformat(date_iso),
        )

    @pytest.mark.django_db
    def login(self, username, password):
        url = '/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', status.HTTP_200_OK),
        ('support_contact', 'test', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', status.HTTP_200_OK),
        ('anonymous_user', 'test', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_contract(self, username, password, status_code):
        self.login(username, password)
        url = '/contracts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(2)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', status.HTTP_201_CREATED),
        ('support_contact', 'test', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', status.HTTP_201_CREATED),
        ('anonymous_user', 'test', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_contract(self, username, password, status_code):
        self.login(username, password)
        url = '/contracts/'
        if username == 'sales_contact' or username == 'staff_contact':
            user = User.objects.get(username='sales_contact')
            sales_contact = SalesContact.objects.get(user=user)
            client = Client.objects.get(first_name="first_name", last_name="last_name")
            date_iso = "2021-12-24 00:00:00.000+00:00"
            data = {'status': False,
                    'amount': 1000.00,
                    'payment_due': datetime.fromisoformat(date_iso),
                    'client_id': client.id,
                    'sales_contact_id': sales_contact.id}
        else:
            data = {}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(3)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', True, 2000.00, '2021-12-15 00:00:00.000+00:00', status.HTTP_200_OK),
        ('support_contact', 'test', False, 0.00, '2021-12-15 00:00:00.000+00:00', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', True, 2500.00, '2021-12-30 00:00:00.000+00:00', status.HTTP_200_OK),
        ('anonymous_user', 'test', True, 2000.00, '2021-12-15 00:00:00.000+00:00', status.HTTP_403_FORBIDDEN),
    ])
    def test_change_contract(self, username, password, new_status, new_amount, new_date_iso, status_code):
        self.login(username, password)
        url = '/contracts/1/'
        if username == 'sales_contact' or username == 'staff_contact':
            contract = Contract.objects.get(pk=1)
            data = ContractSerializer(contract).data
            data['status'] = new_status
            data['amount'] = new_amount
            data['payment_due'] = datetime.fromisoformat(new_date_iso)
        else:
            data = {}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['status'], new_status)
            self.assertEqual(float(response.data['amount']), new_amount)
            self.assertEqual(datetime.fromisoformat(response.data['payment_due']), datetime.fromisoformat(new_date_iso))

    @pytest.mark.order(4)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact', 'test', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', 1, status.HTTP_204_NO_CONTENT),
        ('anonymous_user', 'test', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_contract(self, username, password, pk, status_code):
        self.login(username, password)
        url = f'/contracts/{pk}/'
        response = self.client.delete(url, data='', content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_204_NO_CONTENT:
            self.assertEqual(Contract.objects.count(), 0)
        else:
            self.assertEqual(Contract.objects.count(), 1)


class EventViewTest(TestCase):
    fixtures = ['contenttype.json', 'group.json', 'permission.json', 'eventstatus.json']

    @classmethod
    def setUpTestData(cls):
        # Create users
        User.objects.create_user(
            username='sales_contact',
            password='test',
        )
        sales_contact = SalesContact.objects.create(user=User.objects.get(username='sales_contact'))
        client = Client.objects.create(first_name="test event",
                                       last_name="client",
                                       email="first.client@example.com",
                                       sales_contact=sales_contact)
        User.objects.create_user(
            username='support_contact',
            password='test',
        )
        support_contact = SupportContact.objects.create(user=User.objects.get(username='support_contact'))
        User.objects.create_user(
            username='staff_contact',
            password='test',
        )
        StaffContact.objects.create(user=User.objects.get(username='staff_contact'))
        User.objects.create_user(
            username='anonymous_user',
            password='test',
        )
        date_iso = "2021-12-01 00:00:00.000+00:00"
        Event.objects.create(
            support_contact=support_contact,
            client=client,
            event_status=EventStatus.objects.get(status="C"),
            attendees=1000,
            event_date=datetime.fromisoformat(date_iso),
            notes="test event",
        )

    @pytest.mark.django_db
    def login(self, username,password):
        url = '/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', status.HTTP_200_OK),
        ('support_contact', 'test', status.HTTP_200_OK),
        ('staff_contact', 'test', status.HTTP_200_OK),
        ('anonymous_user', 'test', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_event(self, username,password, status_code):
        self.login(username,password)
        url = '/events/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(2)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', status.HTTP_201_CREATED),
        ('support_contact', 'test', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', status.HTTP_201_CREATED),
        ('anonymous_user', 'test', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_event(self, username,password, status_code):
        self.login(username,password)
        url = '/events/'
        if username == 'sales_contact' or username == 'staff_contact':
            user = User.objects.get(username='support_contact')
            support_contact = SupportContact.objects.get(user=user)
            client = Client.objects.get(first_name="test event", last_name="client")
            date_iso = "2021-12-01 00:00:00.000+00:00"
            data = {'attendees': 700,
                    'notes': "test event",
                    'event_date': datetime.fromisoformat(date_iso),
                    'client_id': client.id,
                    'event_status_id': EventStatus.objects.get(status="C").id,
                    'support_contact_id': support_contact.id}
        else:
            data = {}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(3)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', "P", 200, 'new notes', '2021-12-15 00:00:00.000+00:00', status.HTTP_200_OK),
        ('support_contact', 'test', "E", 0, '', '2021-12-15 00:00:00.000+00:00', status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', "P", 500, 'event in progress', '2021-12-30 00:00:00.000+00:00', status.HTTP_200_OK),
        ('anonymous_user', 'test', "E", 200, '', '2021-12-15 00:00:00.000+00:00', status.HTTP_403_FORBIDDEN),
    ])
    def test_change_event(self, username,password, new_status, new_attendees, new_notes, new_date_iso, status_code):
        self.login(username,password)
        url = '/events/1/'
        if username == 'sales_contact' or username == 'staff_contact':
            event = Event.objects.get(pk=1)
            data = EventSerializer(event).data
            data['event_status_id'] = EventStatus.objects.get(status=new_status).id
            data['attendees'] = new_attendees
            data['notes'] = new_notes
            data['event_date'] = datetime.fromisoformat(new_date_iso)
        else:
            data = {}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['event_status_id'], EventStatus.objects.get(status=new_status).id)
            self.assertEqual(int(response.data['attendees']), new_attendees)
            self.assertEqual(response.data['notes'], new_notes)
            self.assertEqual(datetime.fromisoformat(response.data['event_date']), datetime.fromisoformat(new_date_iso))

    @pytest.mark.order(4)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact', 'test', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact', 'test', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact', 'test', 1, status.HTTP_204_NO_CONTENT),
        ('anonymous_user', 'test', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_event(self, username, password, pk, status_code):
        self.login(username, password)
        url = f'/events/{pk}/'
        response = self.client.delete(url, data='', content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_204_NO_CONTENT:
            self.assertEqual(Event.objects.count(), 0)
        else:
            self.assertEqual(Event.objects.count(), 1)