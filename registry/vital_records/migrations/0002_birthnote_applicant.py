# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-23 13:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vital_records', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='birthnote',
            name='applicant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='vital_records.ApplicantInfo'),
            preserve_default=False,
        ),
    ]