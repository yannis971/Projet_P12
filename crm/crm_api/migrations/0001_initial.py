# Generated by Django 3.2.5 on 2021-08-21 16:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('mobile', models.CharField(blank=True, max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('C', 'CREATED'), ('E', 'ENDED'), ('P', 'IN PROGRESS')], default='C', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='SupportContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SupportContacts',
            },
        ),
        migrations.CreateModel(
            name='StaffContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'StaffContacts',
            },
        ),
        migrations.CreateModel(
            name='SalesContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SalesContacts',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('attendees', models.IntegerField()),
                ('event_date', models.DateTimeField(default=datetime.datetime(2021, 8, 21, 18, 10, 52, 987141))),
                ('notes', models.CharField(blank=True, max_length=2048)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_api.client')),
                ('event_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_api.eventstatus')),
                ('support_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_api.supportcontact')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('payment_due', models.DateTimeField(default=datetime.datetime(2021, 8, 21, 18, 10, 52, 986253))),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_api.client')),
                ('sales_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_api.salescontact')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_api.salescontact'),
        ),
    ]
