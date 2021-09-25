from datetime import datetime

from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class SalesContact(models.Model):
    """
    SalesContact profile
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "SalesContacts"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Overrides save method to save user instance and set user in STAFF Group
        """
        self.user.save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )
        self.user.groups.add(Group.objects.get(name="SALES"))
        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    def __str__(self):
        return self.user.get_username()


class StaffContact(models.Model):
    """
    StaffContact profile
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "StaffContacts"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Overrides save method to save user instance and set user in STAFF Group
        """
        self.user.save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )
        self.user.groups.add(Group.objects.get(name="STAFF"))
        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    def __str__(self):
        return self.user.get_username()


class SupportContact(models.Model):
    """
    SupportContact profile
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "SupportContacts"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        """
        Overrides save method to save user instance
        and set user in SUPPORT Group
        """
        self.user.save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )
        self.user.groups.add(Group.objects.get(name="SUPPORT"))
        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

    def __str__(self):
        return self.user.get_username()


class Client(models.Model):
    """
    Client Entity
    """

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    sales_contact = models.ForeignKey(to=SalesContact, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Contract(models.Model):
    """
    Contrat Entity
    """

    sales_contact = models.ForeignKey(to=SalesContact, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    payment_due = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return (
            f"{self.client} | {self.sales_contact} | {self.status} |"
            f" {self.amount} | {self.payment_due}"
        )


class EventStatus(models.Model):
    """
    EventStatus Entity
    """

    class Status(models.TextChoices):
        CREATED = "C", _("CREATED")
        ENDED = "E", _("ENDED")
        IN_PROGRESS = "P", _("IN PROGRESS")

    status = models.CharField(
        max_length=1, choices=Status.choices, default=Status.CREATED
    )

    def __str__(self):
        return self.get_status_display()


class Event(models.Model):
    """
    Event Entity
    """

    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    support_contact = models.ForeignKey(to=SupportContact, on_delete=models.CASCADE)
    event_status = models.ForeignKey(to=EventStatus, on_delete=models.CASCADE)
    attendees = models.IntegerField()
    event_date = models.DateTimeField(default=datetime.now())
    notes = models.CharField(max_length=2048, blank=True)

    def __str__(self):
        return (
            f"{self.client} | {self.support_contact} | "
            f"{self.event_status} | {self.attendees} | {self.event_date}"
        )
