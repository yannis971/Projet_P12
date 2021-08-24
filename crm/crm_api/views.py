from django.http import request
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

# from crm_api.permissions import IsAuthenticatedStaffMember

from crm_api.serializers import ClientSerializer, ContractSerializer, EventSerializer, UserSerializer

# Create your views here.


@login_required
def home(request):
    context = {
        "welcome": f"Welcome to your dashboard, {request.user.username} !",
        "permissions": request.user.get_all_permissions(),
    }
    return render(request, 'home.html', context=context)

