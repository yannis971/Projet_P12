"""
Module with customized filter_backends
"""
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import BaseFilterBackend

from crm_api.models import (
    Client,
    Contract,
    Event,
    SalesContact,
    StaffContact,
    SupportContact,
)


class Profile:
    """
    Class that defines the profile of a user
    """

    def __init__(self, request):
        """
        Init Profile from request user attribute
        """
        self._user = getattr(request, "user", None)
        try:
            self._staff_contact = StaffContact.objects.get(user=self._user)
        except StaffContact.DoesNotExist:
            self._staff_contact = None
        self._is_staff = bool(self._user.is_superuser or self._staff_contact)
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
        """
        Returns User instance
        """
        return self._user

    @property
    def sales_contact(self):
        """
        Returns SalesContact instance
        """
        return self._sales_contact

    @property
    def support_contact(self):
        """
        Returns SupportContact instance
        """
        return self._support_contact

    @property
    def is_sales(self):
        """
        Returns True if user is a sales contact
        """
        return self._is_sales

    @property
    def is_staff(self):
        """
        Returns True if user is a staff contact
        """
        return self._is_staff

    @property
    def is_support(self):
        """
        Returns True if user is a support contact
        """
        return self._is_support

    @property
    def is_anonymous(self):
        """
        Returns True if user is anonymous
        """
        return not (self._is_sales or self._is_staff or self.is_support)


class ClientFilter(BaseFilterBackend):
    """
    FilterBackend for ClientViewSet
    """

    def filter_queryset(self, request, queryset, view=None):
        """
        Overides filter_queryset method according to the app specifications
        """
        the_profile = Profile(request)
        if the_profile.is_anonymous:
            raise PermissionDenied
        elif the_profile.is_staff:
            # liste de tous les clients
            return queryset.order_by("id")
        elif the_profile.is_sales:
            # liste des clients rattachés à sales_contact
            sales_contact = the_profile.sales_contact
            return queryset.filter(sales_contact=sales_contact).order_by(
                "id"
            )
        elif the_profile.is_support:
            # liste des clients rattachés aux événements
            # attribués à support_contact
            list_client_id = [
                q["client_id"]
                for q in Event.objects.filter(
                    support_contact=the_profile.support_contact
                ).values("client_id")
            ]
            return queryset.filter(Q(id__in=list_client_id)).order_by("id")
        else:
            # queryset vide
            return Client.objects.none()


class ContractFilter(BaseFilterBackend):
    """
    FilterBackend for ContractViewSet
    """

    def filter_queryset(self, request, queryset, view=None):
        """
        Overides filter_queryset method according to the app specifications
        """
        the_profile = Profile(request)
        if the_profile.is_staff:
            # liste de tous les contrats
            return queryset.order_by("id")
        elif the_profile.is_sales:
            # liste des contrats suivis par sales_contact
            # ou rattachés aux clients suivis par sales_contacts
            list_client_id = [
                q["id"]
                for q in Client.objects.filter(
                    sales_contact=the_profile.sales_contact
                ).values("id")
            ]
            return queryset.filter(
                Q(sales_contact=the_profile.sales_contact)
                | Q(client_id__in=list_client_id)
            ).order_by("id")
        else:
            # les autres profils n'ont pas accès aux contrats
            raise PermissionDenied


class EventFilter(BaseFilterBackend):
    """
    FilterBackend for EventViewSet
    """

    def filter_queryset(self, request, queryset, view=None):
        """
        Overides filter_queryset method according to the app specifications
        """
        the_profile = Profile(request)
        if the_profile.is_anonymous:
            raise PermissionDenied
        elif the_profile.is_staff:
            # liste de tous les événements
            return queryset.order_by("id")
        elif the_profile.is_sales:
            # liste des événements des clients
            # ou des contrats suivis par sales_contacts
            list_client_id = [
                q["client_id"]
                for q in Contract.objects.filter(
                    sales_contact=the_profile.sales_contact
                ).values("client_id")
            ]
            return queryset.filter(
                Q(
                    client__in=Client.objects.filter(
                        sales_contact=the_profile.sales_contact
                    )
                )
                | Q(client_id__in=list_client_id)
            ).order_by("id")
        elif the_profile.is_support:
            return queryset.filter(
                support_contact=the_profile.support_contact
            ).order_by("id")
        else:
            return Event.objects.none()
