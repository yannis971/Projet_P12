"""
Module loaddatabase.py
"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import (
    Group,
    Permission
)
from django.core import management
from django.db.models import Q


class Command(management.base.BaseCommand):
    help = 'Load database for EPIC Events application'

    def auth_create_data(self):
        """
        Load data in auth app
        """

        self.stdout.write(self.style.SUCCESS("Start loading data in 'auth'"))
        self.stdout.write(self.style.SUCCESS("Loading data in 'auth.Group'"))
        content_type = ContentType.objects.get(app_label="crm_api", model="contract")
        data = Permission.objects.create(name="Can change contract status",
                                         content_type=content_type,
                                         codename="change_contract_status")
        self.stdout.write(self.style.SUCCESS(f'Load data in model {Permission} : {data}'))

        staff_group = Group.objects.create(name="STAFF")
        content_types = ContentType.objects.filter(Q(app_label="crm_api") | (Q(app_label="auth") & Q(model="user")))
        staff_group.permissions.set(Permission.objects.filter(content_type__in=content_types))
        self.stdout.write(self.style.SUCCESS(f'Load data in model {Group} : {staff_group}'))

        sales_group = Group.objects.create(name="SALES")
        codenames = ('add_client', 'change_client', 'view_client',
                     'add_contract', 'view_contract', 'change_contract_status',
                     'add_event', 'view_event')
        sales_group.permissions.set(Permission.objects.filter(codename__in=codenames))
        self.stdout.write(self.style.SUCCESS(f'Load data in model {Group} : {sales_group}'))

        support_group = Group.objects.create(name="SUPPORT")
        codenames = ('view_client', 'change_event', 'view_event')
        support_group.permissions.set(Permission.objects.filter(codename__in=codenames))
        self.stdout.write(self.style.SUCCESS(f'Load data in model {Group} : {support_group}'))

        self.stdout.write(self.style.SUCCESS("Loading data in 'auth.User'"))
        management.call_command("loaddata", "user.json", verbosity=0)

        self.stdout.write(self.style.SUCCESS("Data have been loaded in 'auth'"))

    def crm_api_create_data(self):
        """
        Load data in crm_api app from fixture "crm_api"
        """
        self.stdout.write(self.style.SUCCESS("Start loading data in 'crm_api'"))
        management.call_command("loaddata", "crm_api.json", verbosity=0)
        self.stdout.write(self.style.SUCCESS("Data have been loaded in 'crm_api'"))

    def handle(self, *args, **options):
        self.auth_create_data()
        self.crm_api_create_data()
        self.stdout.write(self.style.SUCCESS('Data have been loaded successfully'))
