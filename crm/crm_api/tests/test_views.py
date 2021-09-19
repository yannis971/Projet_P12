import pytest

from datetime import datetime
from django.test import TestCase
from rest_framework import status
from crm_api.models import SalesContact, SupportContact, StaffContact, User, Client, Contract, EventStatus, Event
from crm_api.serializers import SalesContactSerializer, SupportContactSerializer, StaffContactSerializer, ClientSerializer, ContractSerializer, EventSerializer

from parameterized import parameterized


class LoginInterface:

    @pytest.mark.django_db
    def login(self, username, password):
        url = '/login/'
        data = {'username': username, 'password': password}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a user
        User.objects.create_user(
            username='test_user',
            password='N3wpolo6',
        )

    @pytest.mark.django_db
    @parameterized.expand([
        ('', '', status.HTTP_400_BAD_REQUEST),
        ('', 'password', status.HTTP_400_BAD_REQUEST),
        ('username', '', status.HTTP_400_BAD_REQUEST),
        ('test_user', 'invalid_password', status.HTTP_403_FORBIDDEN),
        ('test_user', 'N3wpolo6', status.HTTP_200_OK),
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
        ("delete",),
        ("patch", ),
        ("put",),
    ])
    def test_method_not_allowed(self, method):
        url = '/login/'
        response = getattr(self.client, method)(url)
        """
        if method == "delete":
            response = self.client.delete(url)
        elif method == "put":
            response = self.client.put(url)
        else:
            response = self.client.patch(url)
        """
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


class SalesContactViewTest(TestCase, LoginInterface):

    fixtures = ['contenttype.json', 'group.json', 'permission.json', 'user.json', 'salescontact.json', 'staffcontact.json', 'supportcontact.json']

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_salescontact(self, username, password, status_code):
        self.login(username, password)
        url = '/salescontacts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(2)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_201_CREATED),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_salescontact(self, username, password, status_code):
        self.login(username, password)
        url = '/salescontacts/'
        data = {'user': {'username': "sales_contact_02", 'password': "N3wpolo6"}}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(3)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 'Tk1nt3r0K', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 'Tk1nt3r0K', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 'Tk1nt3r0K', 1, status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', 'Tk1nt3r0K', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_change_salescontact(self, username, password, new_password, pk, status_code):
        self.login(username, password)
        url = f'/salescontacts/{pk}/'
        sales_contact = SalesContact.objects.get(pk=pk)
        data = {'user': {'password': new_password} }
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            self.login(sales_contact.user.username, new_password)

    @pytest.mark.order(4)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 1, status.HTTP_204_NO_CONTENT),
        ('anonymous_user', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_salescontact(self, username, password, pk, status_code):
        self.login(username, password)
        url = f'/salescontacts/{pk}/'
        sales_contact = SalesContact.objects.get(pk=pk)
        data = SalesContactSerializer(sales_contact).data
        response = self.client.delete(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_204_NO_CONTENT:
            with self.assertRaises(SalesContact.DoesNotExist):
                SalesContact.objects.get(pk=pk)


class SupportContactViewTest(TestCase, LoginInterface):

    fixtures = ['contenttype.json', 'group.json', 'permission.json', 'user.json', 'salescontact.json', 'staffcontact.json', 'supportcontact.json']

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_supportcontact(self, username, password, status_code):
        self.login(username, password)
        url = '/supportcontacts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(2)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_201_CREATED),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_supportcontact(self, username, password, status_code):
        self.login(username, password)
        url = '/supportcontacts/'
        data = {'user': {'username': "support_contact_02", 'password': "N3wpolo6"}}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(3)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 'C1troenC4', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 'C1troenC4', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 'C1troenC4', 1, status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', 'C1troenC4', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_change_supportcontact(self, username, password, new_password, pk, status_code):
        self.login(username, password)
        url = f'/supportcontacts/{pk}/'
        support_contact = SupportContact.objects.get(pk=pk)
        data = {'user': {'username': support_contact.user.username, 'password': new_password}}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(4)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 1, status.HTTP_204_NO_CONTENT),
        ('anonymous_user', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_supportcontact(self, username, password, pk, status_code):
        self.login(username, password)
        url = f'/supportcontacts/{pk}/'
        support_contact = SupportContact.objects.get(pk=pk)
        data = SupportContactSerializer(support_contact).data
        response = self.client.delete(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_204_NO_CONTENT:
            with self.assertRaises(SupportContact.DoesNotExist):
                SupportContact.objects.get(pk=pk)


class StaffContactViewTest(TestCase, LoginInterface):

    fixtures = ['contenttype.json', 'group.json', 'permission.json', 'user.json', 'salescontact.json', 'staffcontact.json', 'supportcontact.json']

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_staffcontact(self, username, password, status_code):
        self.login(username, password)
        url = '/staffcontacts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(2)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_201_CREATED),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_staffcontact(self, username, password, status_code):
        self.login(username, password)
        url = '/staffcontacts/'
        data = {'user': {'username': "staff_contact_02", 'password': "N3wpolo6"}}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(3)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 'C1troenC5', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 'C1troenC5', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6',  'C1troenC5', 1, status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', 'C1troenC5', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_change_staffcontact(self, username, password, new_password, pk, status_code):
        self.login(username, password)
        url = f'/staffcontacts/{pk}/'
        staff_contact = StaffContact.objects.get(pk=pk)
        data = {'user': {'username': staff_contact.user.username,'password': new_password}}
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(4)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 1, status.HTTP_204_NO_CONTENT),
        ('anonymous_user', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_staffcontact(self, username, password, pk, status_code):
        self.login(username, password)
        url = f'/staffcontacts/{pk}/'
        staff_contact = StaffContact.objects.get(pk=pk)
        data = StaffContactSerializer(staff_contact).data
        response = self.client.delete(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_204_NO_CONTENT:
            with self.assertRaises(StaffContact.DoesNotExist):
                StaffContact.objects.get(pk=pk)


class ClientViewTest(TestCase, LoginInterface):

    fixtures = ['contenttype.json', 'group.json', 'permission.json', 'user.json', 'salescontact.json', 'staffcontact.json', 'supportcontact.json', 'client.json']

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('support_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_client(self, username, password, status_code):
        self.login(username, password)
        url = '/clients/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(2)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_201_CREATED),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_201_CREATED),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_client(self, username, password, status_code):
        self.login(username, password)
        url = '/clients/'
        sales_contact = SalesContact.objects.get(pk=1)
        data = {'first_name': 'new client',
                'last_name': f'by {sales_contact.user.username}',
                'email': 'second.client@example.com',
                'phone': '',
                'mobile': '',
                'sales_contact_id': sales_contact.id}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(3)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 1, '33489916502', '33786753421', status.HTTP_200_OK),
        ('support_contact_01', 'N3wpolo6', 1, '', '', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 1, '33145913572', '33646258429', status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', 1, '', '', status.HTTP_403_FORBIDDEN),
    ])
    def test_change_client(self, username, password, pk, new_phone, new_mobile, status_code):
        self.login(username, password)
        url = f'/clients/{pk}/'
        client = Client.objects.get(pk=pk)
        data = ClientSerializer(client).data
        data['phone'] = new_phone
        data['mobile'] = new_mobile
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['phone'], new_phone)
            self.assertEqual(response.data['mobile'], new_mobile)

    @pytest.mark.order(4)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 1, status.HTTP_204_NO_CONTENT),
        ('anonymous_user', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_client(self, username, password, pk, status_code):
        self.login(username, password)
        url = f'/clients/{pk}/'
        response = self.client.delete(url, data='', content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_204_NO_CONTENT:
            with self.assertRaises(Client.DoesNotExist):
                Client.objects.get(pk=pk)


class ContractViewTest(TestCase, LoginInterface):

    fixtures = ['contenttype.json', 'group.json', 'permission.json', 'user.json', 'salescontact.json', 'staffcontact.json', 'supportcontact.json', 'client.json', 'contract.json']

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_contract(self, username, password, status_code):
        self.login(username, password)
        url = '/contracts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(2)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_201_CREATED),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_201_CREATED),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_contract(self, username, password, status_code):
        self.login(username, password)
        url = '/contracts/'
        client = Client.objects.get(pk=1)
        data = {'status': False,
                'amount': 1000.00,
                'payment_due': datetime.fromisoformat("2021-12-24 00:00:00.000+00:00"),
                'client_id': client.id,
                'sales_contact_id': client.sales_contact.id}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(3)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 1, True, 2000.00, '2021-12-15 00:00:00.000+00:00', status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 1, False, 0.00, '2021-12-15 00:00:00.000+00:00', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 1, True, 2500.00, '2021-12-30 00:00:00.000+00:00', status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', 1, True, 2000.00, '2021-12-15 00:00:00.000+00:00', status.HTTP_403_FORBIDDEN),
    ])
    def test_change_contract(self, username, password, pk, new_status, new_amount, new_date_iso, status_code):
        self.login(username, password)
        url = f'/contracts/{pk}/'
        contract = Contract.objects.get(pk=pk)
        data = ContractSerializer(contract).data
        data['status'] = new_status
        data['amount'] = new_amount
        data['payment_due'] = datetime.fromisoformat(new_date_iso)
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['status'], new_status)
            self.assertEqual(float(response.data['amount']), new_amount)
            self.assertEqual(datetime.fromisoformat(response.data['payment_due']), datetime.fromisoformat(new_date_iso))

    @pytest.mark.order(4)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 1, status.HTTP_204_NO_CONTENT),
        ('anonymous_user', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_contract(self, username, password, pk, status_code):
        self.login(username, password)
        url = f'/contracts/{pk}/'
        response = self.client.delete(url, data='', content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_204_NO_CONTENT:
            with self.assertRaises(Contract.DoesNotExist):
                Contract.objects.get(pk=pk)



class EventViewTest(TestCase, LoginInterface):

    fixtures = ['contenttype.json', 'group.json', 'permission.json', 'eventstatus.json',  'user.json', 'salescontact.json', 'staffcontact.json', 'supportcontact.json', 'client.json', 'contract.json', 'event.json']

    @pytest.mark.order(1)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('support_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_view_event(self, username,password, status_code):
        self.login(username,password)
        url = '/events/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(2)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', status.HTTP_201_CREATED),
        ('support_contact_01', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', status.HTTP_201_CREATED),
        ('anonymous_user', 'N3wpolo6', status.HTTP_403_FORBIDDEN),
    ])
    def test_add_event(self, username,password, status_code):
        self.login(username, password)
        url = '/events/'
        data = {'attendees': 700,
                'notes': "test event",
                'event_date': datetime.fromisoformat("2021-12-01 00:00:00.000+00:00"),
                'client_id': 1,
                'event_status_id': 1,
                'support_contact_id': 1}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)

    @pytest.mark.order(3)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 1, "IN PROGRESS", 200, 'new notes', '2021-12-15 00:00:00.000+00:00', status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 1,  "ENDED", 300, '', '2021-12-15 00:00:00.000+00:00', status.HTTP_200_OK),
        ('staff_contact_01', 'N3wpolo6', 1, "IN PROGRESS", 500, 'event in progress', '2021-12-30 00:00:00.000+00:00', status.HTTP_200_OK),
        ('anonymous_user', 'N3wpolo6', 1, "ENDED", 200, '', '2021-12-15 00:00:00.000+00:00', status.HTTP_403_FORBIDDEN),
    ])
    def test_change_event(self, username, password, pk, new_event_status, new_attendees, new_notes, new_date_iso, status_code):
        self.login(username,password)
        url = f'/events/{pk}/'
        event = Event.objects.get(pk=pk)
        data = EventSerializer(event).data
        data['event_status'] = {'status': new_event_status}
        data['attendees'] = new_attendees
        data['notes'] = new_notes
        data['event_date'] = datetime.fromisoformat(new_date_iso)
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['event_status']['status'], new_event_status)
            self.assertEqual(int(response.data['attendees']), new_attendees)
            self.assertEqual(response.data['notes'], new_notes)
            self.assertEqual(datetime.fromisoformat(response.data['event_date']), datetime.fromisoformat(new_date_iso))

    @pytest.mark.order(4)
    @pytest.mark.django_db
    @parameterized.expand([
        ('sales_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('support_contact_01', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
        ('staff_contact_01', 'N3wpolo6', 1, status.HTTP_204_NO_CONTENT),
        ('anonymous_user', 'N3wpolo6', 1, status.HTTP_403_FORBIDDEN),
    ])
    def test_delete_event(self, username, password, pk, status_code):
        self.login(username, password)
        url = f'/events/{pk}/'
        response = self.client.delete(url, data='', content_type='application/json')
        self.assertEqual(response.status_code, status_code)
        if status_code == status.HTTP_204_NO_CONTENT:
            with self.assertRaises(Event.DoesNotExist):
                Event.objects.get(pk=pk)
