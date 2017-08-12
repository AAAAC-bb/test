# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-11 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='host_groups',
            field=models.ManyToManyField(blank=True, to='audit.HostGroup'),
        ),
        migrations.AlterField(
            model_name='account',
            name='host_user_binds',
            field=models.ManyToManyField(blank=True, to='audit.HostUserBind'),
        ),
    ]
