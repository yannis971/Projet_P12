from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView

from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.views.generic import TemplateView
from django.conf import settings

from django.contrib.auth.signals import user_logged_in
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

from django.contrib.auth.models import User

from crm_api.models import SalesContact, Client, Contract, Event

# from crm_api.permissions import IsAuthenticatedStaffMember

from crm_api.decorators import route_permissions

from crm_api.serializers import ClientSerializer, ContractSerializer, EventSerializer, UserSerializer, SalesContactSerializer

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


"""
class LoginViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                user_details = {}
                user_details['username'] = user.username
                login(request, user)
                return Response(user_details, status=status.HTTP_200_OK)
            else:
                res = {
                    'error': 'can not authenticate with the given credentials \
                    or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a username and a password'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        res = {
            'detail': 'Méthode « GET » non autorisée.'}
        return Response(res, status=status.HTTP_405_METHOD_NOT_ALLOWED)
"""

#class LoginView(LoginView):
class LoginView(generics.GenericAPIView):

    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        print("request :", request)
        print("self :", self)
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                user_details = {}
                user_details['username'] = user.username
                user_details['token'] = token
                login(request, user)
                return Response(user_details, status=status.HTTP_200_OK)
            else:
                res = {
                    'error': 'can not authenticate with the given credentials \
                    or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a username and a password'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(TemplateView):

  template_name = 'crm_api/logged_out.html'

  def get(self, request, **kwargs):

    logout(request)

    return render(request, self.template_name)


class SalesContactViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    """
    class SalesContactViewSet manages the following endpoints :
    /salescontacts/
    /salescontacts/{pk}/
    """
    queryset = SalesContact.objects.all()
    serializer_class = SalesContactSerializer

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
    def delete(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
