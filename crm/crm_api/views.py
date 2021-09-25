""" Module views.py"""

import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import management
from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings


from crm_api.decorators import route_permissions
from crm_api.filters import ClientFilter, ContractFilter, EventFilter
from crm_api.models import (Client, Contract, Event, EventStatus, SalesContact,
                            StaffContact, SupportContact)
from crm_api.permissions import ContractPermission
from crm_api.serializers import (ClientSerializer, ContractSerializer,
                                 EventSerializer, SalesContactSerializer,
                                 StaffContactSerializer,
                                 SupportContactSerializer, User,
                                 UserSerializer)

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Authentification Class to not perform the csrf check previously happening
    """
    def enforce_csrf(self, request):
        return


@login_required
def home(request):
    """
    home view
    """
    context = {
        "welcome": f"Welcome to your dashboard, {request.user.username} !",
        "permissions": request.user.get_all_permissions(),
    }
    return render(request, "crm_api/home.html", context=context)


class LoginView(generics.GenericAPIView):
    """
    LoginView
    Manages the following endpoint:
    /api/login/
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        try:
            username = request.data["username"]
            password = request.data["password"]
            if username and password:
                user = authenticate(username=username, password=password)
                if user and user.is_active:
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    user_details = dict()
                    user_details["username"] = user.username
                    user_details["token"] = token
                    login(request, user)
                    logger.info(msg=f"{self.__class__.__name__} : {user.username} logged in")
                    return Response(user_details, status=status.HTTP_200_OK)
                else:
                    res = {
                        "error": "can not authenticate with the given credentials \
                        or the account has been deactivated"
                    }
                    return Response(res, status=status.HTTP_403_FORBIDDEN)
            else:
                res = {"error": "please provide a username and a password"}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            res = {"error": "please provide a username and a password"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs):
        res = {
            "error": "user should authenticate via /login/ endpoint and POST method providing a username and a password"
        }
        return Response(res, status=status.HTTP_403_FORBIDDEN)


class LogoutView(generics.GenericAPIView):
    """
    LogoutView
    Manages the following endpoint:
    /api/logout/
    """
    def get(self, request, **kwargs):
        details = dict()
        details["username"] = request.user.username
        details["message"] = "Your are now logged out"
        logger.info(msg=f"{self.__class__.__name__} : {request.user.username} logged out")
        logout(request)
        return Response(details, status=status.HTTP_200_OK)


class SalesContactViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    class SalesContactViewSet manages the following endpoints :
    /salescontacts/
    /salescontacts/{pk}/
    """

    queryset = SalesContact.objects.order_by("id")
    serializer_class = SalesContactSerializer
    redirect_field_name = None

    @route_permissions("crm_api.add_salescontact")
    def create(self, request, *args, **kwargs):
        request.data["user"]["groups"] = [
            {"name": "SALES"},
        ]
        return super().create(request, *args, **kwargs)

    @route_permissions("crm_api.view_salescontact")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions("crm_api.view_salescontact")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions("crm_api.change_salescontact")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data["user"]["username"] = instance.user.username
        serializer = self.get_serializer(instance)
        serializer.update(instance, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return super().update(request, *args, **kwargs)

    @route_permissions("crm_api.change_salescontact")
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data["user"]["username"] = instance.user.username
        serializer = self.get_serializer(instance)
        serializer.update(instance, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return super().partial_update(request, *args, **kwargs)

    @route_permissions("crm_api.delete_salescontact")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class SupportContactViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    class SupportContactViewSet manages the following endpoints :
    /supportcontacts/
    /supportcontacts/{pk}/
    """

    queryset = SupportContact.objects.order_by("id")
    serializer_class = SupportContactSerializer
    redirect_field_name = None

    @route_permissions("crm_api.add_supportcontact")
    def create(self, request, *args, **kwargs):
        request.data["groups"] = [
            {"name": "SUPPORT"},
        ]
        return super().create(request, *args, **kwargs)

    @route_permissions("crm_api.view_supportcontact")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions("crm_api.view_supportcontact")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions("crm_api.change_supportcontact")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data["user"]["username"] = instance.user.username
        serializer = self.get_serializer(instance)
        serializer.update(instance, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @route_permissions("crm_api.change_supportcontact")
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data["user"]["username"] = instance.user.username
        serializer = self.get_serializer(instance)
        serializer.update(instance, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @route_permissions("crm_api.delete_supportcontact")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class StaffContactViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    class StaffContactViewSet manages the following endpoints :
    /staffcontacts/
    /staffcontacts/{pk}/
    """

    queryset = StaffContact.objects.order_by("id")
    serializer_class = StaffContactSerializer
    redirect_field_name = None

    @route_permissions("crm_api.add_staffcontact")
    def create(self, request, *args, **kwargs):
        request.data["groups"] = [
            {"name": "STAFF"},
        ]
        return super().create(request, *args, **kwargs)

    @route_permissions("crm_api.view_staffcontact")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions("crm_api.view_staffcontact")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions("crm_api.change_staffcontact")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data["user"]["username"] = instance.user.username
        serializer = self.get_serializer(instance)
        serializer.update(instance, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @route_permissions("crm_api.change_staffcontact")
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        request.data["user"]["username"] = instance.user.username
        serializer = self.get_serializer(instance)
        serializer.update(instance, request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @route_permissions("crm_api.delete_staffcontact")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ClientViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    class ClientViewSet manages the following endpoints :
    /clients/
    /clients/{pk}/
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ClientFilter]
    filterset_fields = [
        "sales_contact",
    ]
    search_fields = ["first_name", "last_name", "email"]
    redirect_field_name = None

    def _prepare_update_client(self, request):
        the_client = self.get_object()
        request.data["sales_contact_id"] = the_client.sales_contact.id

    @route_permissions("crm_api.add_client")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_permissions("crm_api.view_client")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions("crm_api.view_client")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions("crm_api.change_client")
    def update(self, request, *args, **kwargs):
        self._prepare_update_client(request)
        return super().update(request, *args, **kwargs)

    @route_permissions("crm_api.change_client")
    def partial_update(self, request, *args, **kwargs):
        self._prepare_update_client(request)
        return super().partial_update(request, *args, **kwargs)

    @route_permissions("crm_api.delete_client")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ContractViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    class ContractViewSet manages the following endpoints :
    /contracts/
    /contracts/{pk}/
    """

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [
        ContractPermission,
    ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ContractFilter]
    filterset_fields = ["sales_contact", "client"]
    redirect_field_name = None

    def _prepare_update_contract(self, request):
        the_contract = self.get_object()
        request.data["client_id"] = the_contract.client.id
        request.data["sales_contact_id"] = the_contract.sales_contact.id

    @route_permissions("crm_api.add_contract")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_permissions("crm_api.view_contract")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions("crm_api.view_contract")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._prepare_update_contract(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._prepare_update_contract(request)
        return super().partial_update(request, *args, **kwargs)

    @route_permissions("crm_api.delete_contract")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class EventViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    class EventViewSet manages the following endpoints :
    /events/
    /events/{pk}/
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, EventFilter]
    filterset_fields = ["support_contact", "client", "event_status"]
    search_fields = [
        "notes",
    ]
    redirect_field_name = None

    def _prepare_update_event(self, request):
        the_event = self.get_object()
        request.data["client_id"] = the_event.client.id
        request.data["support_contact_id"] = the_event.support_contact.id
        if "event_status" in request.data and "status" in request.data["event_status"]:
            the_event_status = [
                item
                for item in EventStatus.objects.all()
                if item.__str__() == request.data["event_status"]["status"]
            ][0]
            request.data["event_status_id"] = the_event_status.id
        else:
            request.data["event_status_id"] = the_event.event_status.id

    @route_permissions("crm_api.add_event")
    def create(self, request, *args, **kwargs):
        the_event_status = EventStatus.objects.get(status=EventStatus.Status.CREATED)
        request.data["event_status_id"] = the_event_status.id
        return super().create(request, *args, **kwargs)

    @route_permissions("crm_api.view_event")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions("crm_api.view_event")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions("crm_api.change_event")
    def update(self, request, *args, **kwargs):
        self._prepare_update_event(request)
        return super().update(request, *args, **kwargs)

    @route_permissions("crm_api.change_event")
    def partial_update(self, request, *args, **kwargs):
        self._prepare_update_event(request)
        return super().partial_update(request, *args, **kwargs)

    @route_permissions("crm_api.delete_event")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class InitDataBaseView(generics.GenericAPIView):
    """
    Class to init database only for test purpose with postman
    Manages the following endpoint:
    /init_database/
    """
    def get(self, request, **kwargs):
        if request.user and request.user.is_authenticated:
            Event.objects.all().delete()
            EventStatus.objects.all().delete()
            Contract.objects.all().delete()
            Client.objects.all().delete()
            SalesContact.objects.all().delete()
            SupportContact.objects.all().delete()
            StaffContact.objects.all().delete()
            management.call_command("sqlsequencereset", "crm_api", verbosity=0)

            User.objects.all().delete()
            management.call_command("sqlsequencereset", "auth", verbosity=0)

            management.call_command("loaddata", "user.json", verbosity=0)
            management.call_command("loaddata", "crm_api.json", verbosity=0)

            res = {"message": "database has been initialized"}

            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
