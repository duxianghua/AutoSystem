# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-24 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Assets', '0009_auto_20160724_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='servers_info',
            name='host_name',
            field=models.CharField(blank='Ture', max_length=100, null='Ture'),
        ),
    ]
