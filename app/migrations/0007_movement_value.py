# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20171014_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='value',
            field=models.IntegerField(default=1),
        ),
    ]
