"""
Module init_database.py
"""
import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import (
    User,
    Group,
    Permission
)

from django.core import management
from django.db.models import Q


logger = logging.getLogger(__name__)



def auth_create_data():
    """
    Load data in auth app
    """
    logger.info("Load data in auth")
    management.call_command("loaddata", "user.json", verbosity=0)

    content_type = ContentType.objects.get(app_label="crm_api", model="contract")
    data = Permission.objects.create(name="Can change contract status",
                              content_type=content_type,
                              codename="change_contract_status")
    logger.info("Load data in model", Permission, " :", data)

    staff_group = Group.objects.create(name="STAFF")
    content_types = ContentType.objects.filter(Q(app_label="crm_api") | (Q(app_label="auth") & Q(model="user")))
    staff_group.permissions.set(Permission.objects.filter(content_type__in=content_types))
    logger.info("Load data in model", Group, " :", staff_group)

    sales_group = Group.objects.create(name="SALES")
    codenames = ('add_client', 'change_client', 'view_client',
                 'add_contract', 'view_contract', 'change_contract_status',
                 'add_event', 'view_event')
    sales_group.permissions.set(Permission.objects.filter(codename__in=codenames))
    logger.info("Load data in model", Group, " :", sales_group)

    support_group = Group.objects.create(name="SALES")
    codenames = ('view_client', 'change_event', 'view_event')
    support_group.permissions.set(Permission.objects.filter(codename__in=codenames))
    logger.info("Load data in model", Group, " :", support_group)

def auth_delete_data():
    """
    Delete tables in auth app
    """
    data = Group.objects.all().delete
    logger.info("Delete in model", Group, " :", data)
    data = User.objects.all().delete()
    logger.info("Delete in model", User, " :", data)
    data = Permission.objects.get(codename="change_contract_status").delete()
    logger.info("Delete in model", Permission, " :", data)
    management.call_command("sqlsequencereset", "auth", verbosity=0)


def crm_api_create_data():
    """
    Load data in crm_api app from fixture "crm_api"
    """
    logger.info("Load data in crm_api")
    management.call_command("loaddata", "crm_api.json", verbosity=0)


def crm_api_delete_data():
    """
    Delete all tables in crm_api app
    """
    crm_api = apps.get_app_config('crm_api')
    for model in crm_api.get_models():
        data = model.objects.all().delete()
        logger.info("Delete in model", model, " :", data)
    management.call_command("sqlsequencereset", crm_api.name, verbosity=0)


if __name__ == '__main__':
    """
    Main
    """
    crm_api_delete_data()
    auth_delete_data()
    auth_create_data()
    crm_api_create_data()
    update_fixtures()
