# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-21 16:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Salt', '0003_auto_20160721_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salt_info',
            old_name='salt_api_password',
            new_name='salt_api_password1',
        ),
    ]
