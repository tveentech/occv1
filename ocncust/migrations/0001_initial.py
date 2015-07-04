# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocndata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivilegeAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=255)),
                ('tier', models.CharField(max_length=255, blank=True)),
                ('points', models.IntegerField(null=True, blank=True)),
                ('last_updated_at', models.DateField()),
                ('website', models.URLField(max_length=255, blank=True)),
                ('username', models.CharField(max_length=255, blank=True)),
                ('password', models.CharField(max_length=255, blank=True)),
                ('email', models.EmailField(max_length=255, blank=True)),
                ('phone', models.CharField(max_length=255, blank=True)),
                ('dob', models.DateField(null=True, blank=True)),
                ('remarks', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('guest', models.ForeignKey(to='ocndata.Client')),
            ],
        ),
        migrations.CreateModel(
            name='PrivilegeProgram',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('remarks', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='privilegeprogram',
            unique_together=set([('title',)]),
        ),
        migrations.AddField(
            model_name='privilegeaccount',
            name='program_type',
            field=models.ForeignKey(to='ocncust.PrivilegeProgram'),
        ),
        migrations.AlterUniqueTogether(
            name='privilegeaccount',
            unique_together=set([('guest', 'number')]),
        ),
    ]
