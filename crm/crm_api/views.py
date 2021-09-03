from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView

from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.views.generic import TemplateView
from django.conf import settings

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from rest_framework import generics, mixins, views
from rest_framework import status
from rest_framework import viewsets

from rest_framework.exceptions import NotFound, ValidationError

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings

from crm_api.models import SalesContact, Client, Contract, Event

# from crm_api.permissions import IsAuthenticatedStaffMember

from crm_api.decorators import route_permissions

from crm_api.serializers import ClientSerializer, ContractSerializer, EventSerializer, UserSerializer, SalesContactSerializer, User

# Create your views here.

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@login_required
def home(request):
    context = {
        "welcome": f"Welcome to your dashboard, {request.user.username} !",
        "permissions": request.user.get_all_permissions(),
    }
    return render(request, 'crm_api/home.html', context=context)


class LoginView(generics.GenericAPIView):

    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        try:
            username = request.data['username']
            password = request.data['password']
            if username and password:
                user = authenticate(username=username, password=password)
                if user and user.is_active:
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    user_details = dict()
                    user_details['username'] = user.username
                    user_details['token'] = token
                    login(request, user)
                    return Response(user_details, status=status.HTTP_200_OK)
                else:
                    res = {
                        'error': 'can not authenticate with the given credentials \
                        or the account has been deactivated'}
                    return Response(res, status=status.HTTP_403_FORBIDDEN)
            else:
                res = {'error': 'please provide a username and a password'}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            res = {'error': 'please provide a username and a password'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs):
        res = {
            'error': 'user should authenticate via /login/ endpoint and POST method providing a username and a password'}
        return Response(res, status=status.HTTP_403_FORBIDDEN)


class LogoutView(generics.GenericAPIView):

    def get(self, request, **kwargs):
        details = dict()
        details['username'] = request.user.username
        details['message'] = "Your are now logged out"
        logout(request)
        return Response(details, status=status.HTTP_200_OK)


class SalesContactViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    class SalesContactViewSet manages the following endpoints :
    /salescontacts/
    /salescontacts/{pk}/
    """
    queryset = SalesContact.objects.all()
    serializer_class = SalesContactSerializer
    redirect_field_name = None

    @route_permissions('crm_api.add_salescontact')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_permissions('crm_api.view_salescontact')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions('crm_api.view_salescontact')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions('crm_api.change_salescontact')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @route_permissions('crm_api.change_salescontact')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @route_permissions('crm_api.delete_salescontact')
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
    redirect_field_name = None


    @route_permissions('crm_api.add_client')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_permissions('crm_api.view_client')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions('crm_api.view_client')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions('crm_api.change_client')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @route_permissions('crm_api.change_client')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @route_permissions('crm_api.delete_client')
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
    redirect_field_name = None

    @route_permissions('crm_api.add_contract')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_permissions('crm_api.view_contract')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions('crm_api.view_contract')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions('crm_api.change_contract')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @route_permissions('crm_api.change_contract')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @route_permissions('crm_api.delete_contract')
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
    redirect_field_name = None

    @route_permissions('crm_api.add_event')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @route_permissions('crm_api.view_event')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @route_permissions('crm_api.view_event')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @route_permissions('crm_api.change_event')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @route_permissions('crm_api.change_event')
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @route_permissions('crm_api.delete_event')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)