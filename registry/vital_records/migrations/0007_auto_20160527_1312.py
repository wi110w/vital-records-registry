# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-27 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vital_records', '0006_auto_20160526_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthnote',
            name='note_number',
            field=models.PositiveIntegerField(unique=True, verbose_name='note number'),
        ),
    ]
