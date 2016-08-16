# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-24 05:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Assets', '0008_auto_20160722_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='host_status',
            field=models.CharField(default='Active', max_length=16),
        ),
        migrations.AddField(
            model_name='host',
            name='salt_key_name',
            field=models.CharField(default='UNknow', max_length=100),
        ),
    ]
