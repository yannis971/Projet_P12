"""
Module initdatabase.py
"""
from django.apps import apps
from django.contrib.auth.models import (
    User,
    Group,
    Permission
)

from django.core import management


class Command(management.base.BaseCommand):
    help = 'Initialize database for EPIC Events application'

    def auth_delete_data(self):
        """
        Delete tables in auth app
        """
        data = Group.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Delete in model {Group} : {data}'))
        data = User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Delete in model {User} : {data}'))
        try:
            data = Permission.objects.get(codename="change_contract_status").delete()
            self.stdout.write(self.style.SUCCESS(f'Delete in model {Permission} : {data}'))
        except Permission.DoesNotExist:
            self.stdout.write('Permission with codename="change_contract_status" does not exist')

    def crm_api_delete_data(self):
        """
        Delete all tables in crm_api app
        """
        crm_api = apps.get_app_config('crm_api')
        for model in crm_api.get_models():
            data = model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Delete in model {model} : {data}'))

    def handle(self, *args, **options):
        self.crm_api_delete_data()
        self.auth_delete_data()
        self.stdout.write(self.style.SUCCESS('Data have been initialized successfully'))
