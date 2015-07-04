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
            name='CreditCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issuing_bank', models.CharField(max_length=255)),
                ('card_type', models.CharField(max_length=50, choices=[(b'Visa', b'Visa'), (b'Master Card', b'Master Card'), (b'American Express', b'American Express')])),
                ('card_number', models.CharField(max_length=50)),
                ('name_on_card', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=255)),
                ('website', models.URLField(max_length=255, blank=True)),
                ('username', models.CharField(max_length=255, blank=True)),
                ('password', models.CharField(max_length=255, blank=True)),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('phone', models.CharField(max_length=255, blank=True)),
                ('pending_amount', models.DecimalField(default=0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('current_available_amount', models.DecimalField(default=0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('actual_available_amount', models.DecimalField(default=0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('total_limit', models.DecimalField(default=0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('next_statement_generation_date', models.DateField(null=True, blank=True)),
                ('next_payment_date', models.DateField(null=True, blank=True)),
                ('credit_days_available', models.IntegerField(default=0, null=True, blank=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('remarks', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_updated_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-is_active', '-credit_days_available', '-actual_available_amount'],
            },
        ),
        migrations.CreateModel(
            name='OnlineSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('website', models.URLField(max_length=255, blank=True)),
                ('agent_id', models.CharField(max_length=255, blank=True)),
                ('agent_password', models.CharField(max_length=255, blank=True)),
                ('user_id', models.CharField(max_length=255, blank=True)),
                ('user_password', models.CharField(max_length=255, blank=True)),
                ('product_type', models.CharField(help_text=b'Separate multiple products by comma', max_length=255, blank=True)),
                ('destination', models.CharField(max_length=255, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('remarks', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(related_name='online_system_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(related_name='online_system_last_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='onlinesystem',
            unique_together=set([('title',)]),
        ),
        migrations.AlterUniqueTogether(
            name='creditcard',
            unique_together=set([('card_number',)]),
        ),
    ]
