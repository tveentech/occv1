# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentReminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_title', models.CharField(max_length=255)),
                ('payment_due_date', models.DateField(help_text=b'YYYY-MM-DD')),
                ('currency_type', models.CharField(help_text=b'INR, USD, EUR, AUD, SGD, etc', max_length=255)),
                ('amount', models.DecimalField(help_text=b'12345.78', max_digits=10, decimal_places=2)),
                ('remarks', models.TextField(blank=True)),
                ('payment_date', models.DateField(help_text=b'YYYY-MM-DD', null=True, blank=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_void', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('payment_owner', models.ForeignKey(related_name='payment_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['is_void', 'is_paid', 'payment_due_date'],
            },
        ),
    ]
