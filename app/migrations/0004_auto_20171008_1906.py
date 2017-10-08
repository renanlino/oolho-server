# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 22:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20171008_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensor',
            old_name='created_by',
            new_name='owner',
        ),
        migrations.AlterField(
            model_name='sensor',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]