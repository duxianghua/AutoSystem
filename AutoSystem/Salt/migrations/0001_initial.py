# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 14:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salt_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=16)),
                ('Area_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Assets.Area')),
            ],
        ),
    ]
