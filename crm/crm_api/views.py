
from django.contrib.auth.signals import user_logged_in
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets

from rest_framework.exceptions import NotFound, ValidationError

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.auth.models import User

from crm_api.models import Client, Contract, Event

from crm_api.permissions import IsAuthenticatedStaffMember

from crm_api.serializers import ClientSerializer, ContractSerializer, EventSerializer, UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    User viewset to create, read, update, delete a user
    Permission : restricted to Staff team members only
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedStaffMember, ]


class LoginViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    class LoginViewSet manages the following endpoint :
    /login/
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            print("username :", username)
            print("password :", password)
            user = get_object_or_404(User, username=username, password=password)
            if user:
                try:
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)
                except Exception as e:
                    raise e
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
