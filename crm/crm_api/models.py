from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.


class SalesContact(User):
    class Meta:
        db_table = "SalesContacts"


class StaffContact(User):
    class Meta:
        db_table = "StaffContacts"


class SupportContact(User):
    class Meta:
        db_table = "SupportContacts"


class Client(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(to=SalesContact, on_delete=models.CASCADE)


class Contract(models.Model):
    sales_contact = models.ForeignKey(to=SalesContact, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    payment_due = models.DateTimeField(default=datetime.now())


class EventStatus(models.Model):
    class Status(models.TextChoices):
        CREATED = 'C', _('CREATED')
        ENDED = 'E', _('ENDED')
        IN_PROGRESS = 'P', _('IN PROGRESS')
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.CREATED)


class Event(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(to=SupportContact, on_delete=models.CASCADE)
    event_status = models.ForeignKey(to=EventStatus, on_delete=models.CASCADE)
    attendees = models.IntegerField()
    event_date = models.DateTimeField(default=datetime.now())
    notes = models.CharField(max_length=2048, blank=True)
