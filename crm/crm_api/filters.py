import django_filters
from django.db.models import Q
from crm_api.models import SalesContact, StaffContact,SupportContact,Client,Contract,Event
from rest_framework.filters import BaseFilterBackend
from rest_framework.exceptions import PermissionDenied


class Profile:

    def __init__(self, request):
        self._user = getattr(request, 'user', None)
        try:
            self._staff_contact = StaffContact.objects.get(user=self._user)
        except StaffContact.DoesNotExist:
            self._staff_contact = None
        self._is_staff = bool(self._user.is_staff or self._staff_contact)
        try:
            self._sales_contact = SalesContact.objects.get(user=self._user)
        except SalesContact.DoesNotExist:
            self._sales_contact = None
        self._is_sales = bool(self._sales_contact)
        try:
            self._support_contact = SupportContact.objects.get(user=self._user)
        except SupportContact.DoesNotExist:
            self._support_contact = None
        self._is_support = bool(self._support_contact)

    @property
    def user(self):
        return self._user

    @property
    def sales_contact(self):
        return self._sales_contact

    @property
    def support_contact(self):
        return self._support_contact

    @property
    def is_sales(self):
        return self._is_sales

    @property
    def is_staff(self):
        return self._is_staff

    @property
    def is_support(self):
        return self._is_support

    @property
    def is_anonymous(self):
        return not(self._is_sales or self._is_staff or self.is_support)


class ClientFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view=None):
        the_profile = Profile(request)
        if the_profile.is_anonymous:
            raise PermissionDenied
        elif the_profile.is_staff:
            # liste de tous les clients
            return queryset.order_by('id')
        elif the_profile.is_sales:
            # liste des clients rattachés à sales_contact
            return queryset.filter(sales_contact=the_profile.sales_contact).order_by('id')
        elif the_profile.is_support:
            # liste des clients rattachés aux événements attribués à support_contact
            list_client_id = [q['client_id'] for q in
                              Event.objects.filter(support_contact=the_profile.support_contact).values('client_id')]
            return queryset.filter(Q(id__in=list_client_id)).order_by('id')
        else:
            # queryset vide
            return Client.objects.none()


class ContractFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view=None):
        the_profile = Profile(request)
        if the_profile.is_staff:
            # liste de tous les contrats
            return queryset.order_by('id')
        elif the_profile.is_sales:
            # liste des contrats suivis par sales_contact ou rattachés aux clients suivis par sales_contacts
            list_client_id = [q['id'] for q in
                              Client.objects.filter(sales_contact=the_profile.sales_contact).values('id')]
            return queryset.filter(Q(sales_contact=the_profile.sales_contact) | Q(client_id__in=list_client_id)).order_by('id')
        else:
            # les autres profils n'ont pas accès aux contrats
            raise PermissionDenied


class EventFilter(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view=None):
        the_profile = Profile(request)
        if the_profile.is_anonymous:
            raise PermissionDenied
        elif the_profile.is_staff:
            # liste de tous les événements
            return queryset.order_by('id')
        elif the_profile.is_sales:
            # liste des événements des clients ou des contrats suivis par sales_contacts
            list_client_id = [q['client_id'] for q in
                              Contract.objects.filter(sales_contact=the_profile.sales_contact).values('client_id')]
            return queryset.filter(Q(client__in=Client.objects.filter(sales_contact=the_profile.sales_contact)) |
                                 Q(client_id__in=list_client_id)).order_by('id')
        elif the_profile.is_support:
            return queryset.filter(support_contact=the_profile.support_contact).order_by('id')
        else:
            return Event.objects.none()
