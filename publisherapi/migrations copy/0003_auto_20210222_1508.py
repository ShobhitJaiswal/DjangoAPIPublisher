# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-02-22 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisherapi', '0002_publisher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publisher',
            name='Name',
        ),
        migrations.RemoveField(
            model_name='publisher',
            name='URL',
        ),
        migrations.AddField(
            model_name='publisher',
            name='api',
            field=models.CharField(default=None, max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publisher',
            name='api_parameters',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publisher',
            name='name',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publisher',
            name='url',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
