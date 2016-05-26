# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-26 20:48
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import vital_records.models
import vital_records.validators


class Migration(migrations.Migration):

    dependencies = [
        ('vital_records', '0005_auto_20160519_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthnote',
            name='birth_date',
            field=models.DateField(validators=[vital_records.validators.MaxCallableValidator(limit_callable=vital_records.models._today, message='Birth date cannot be future')], verbose_name='date of birth'),
        ),
        migrations.AlterField(
            model_name='birthnote',
            name='child_number',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message="Child number can't be zero")], verbose_name='child number'),
        ),
        migrations.AlterField(
            model_name='birthnote',
            name='children_born_count',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message="Children born count can't be zero")], verbose_name='children born count'),
        ),
        migrations.AlterField(
            model_name='note',
            name='compose_date',
            field=models.DateField(blank=True, validators=[vital_records.validators.MaxCallableValidator(limit_callable=vital_records.models._today, message='Note record compose date cannot be future')], verbose_name='note record compose date'),
        ),
        migrations.AlterField(
            model_name='person',
            name='family_status',
            field=models.BooleanField(default=False, verbose_name='family status'),
        ),
    ]