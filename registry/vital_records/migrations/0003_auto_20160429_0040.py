# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 21:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vital_records', '0002_birthnote_applicant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicantinfo',
            options={'verbose_name': 'Applicant information', 'verbose_name_plural': 'Applicants information'},
        ),
        migrations.AlterModelOptions(
            name='birthevidence',
            options={'verbose_name': 'Birth evidence', 'verbose_name_plural': 'Birth evidences'},
        ),
        migrations.AlterModelOptions(
            name='birthnote',
            options={'verbose_name': 'Birth note record', 'verbose_name_plural': 'Birth note records'},
        ),
        migrations.AlterModelOptions(
            name='birthnotelaw',
            options={'verbose_name': 'Birth related law', 'verbose_name_plural': 'Birth related laws'},
        ),
        migrations.AlterModelOptions(
            name='birthplace',
            options={'verbose_name': 'Birth place', 'verbose_name_plural': 'Birth places'},
        ),
        migrations.AlterModelOptions(
            name='deathevidence',
            options={'verbose_name': 'Death evidence', 'verbose_name_plural': 'Death evidences'},
        ),
        migrations.AlterModelOptions(
            name='deathnote',
            options={'verbose_name': 'Death note record', 'verbose_name_plural': 'Death note records'},
        ),
        migrations.AlterModelOptions(
            name='deathplace',
            options={'verbose_name': 'Death place', 'verbose_name_plural': 'Death places'},
        ),
        migrations.AlterModelOptions(
            name='document',
            options={'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
        migrations.AlterModelOptions(
            name='marriagenote',
            options={'verbose_name': 'Marriage note record', 'verbose_name_plural': 'Marriage note records'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Person', 'verbose_name_plural': 'Persons'},
        ),
        migrations.AlterModelOptions(
            name='registrar',
            options={'verbose_name': 'Registrar', 'verbose_name_plural': 'Registrars'},
        ),
        migrations.AlterModelOptions(
            name='residence',
            options={'verbose_name': 'Residence info', 'verbose_name_plural': 'Residences'},
        ),
        migrations.RemoveField(
            model_name='note',
            name='status',
        ),
        migrations.AddField(
            model_name='note',
            name='was_revoked',
            field=models.BooleanField(default=False, verbose_name='was revoked'),
        ),
        migrations.AlterField(
            model_name='applicantinfo',
            name='last_name',
            field=models.CharField(max_length=64, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='birthnote',
            name='child_gender',
            field=models.BooleanField(choices=[(True, 'Male'), (False, 'Female')], default=False, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='note',
            name='compose_date',
            field=models.DateField(blank=True, verbose_name='note record compose date'),
        ),
        migrations.AlterField(
            model_name='note',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.BooleanField(choices=[(True, 'Male'), (False, 'Female')], verbose_name='gender'),
        ),
        migrations.RenameField(
            model_name='applicantinfo',
            old_name='name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AlterField(
            model_name='applicantinfo',
            name='first_name',
            field=models.CharField(max_length=64, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='applicantinfo',
            name='last_name',
            field=models.CharField(max_length=64, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=64, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.BooleanField(choices=[(True, 'Male'), (False, 'Female')], default=False, verbose_name='gender'),
        ),
    ]
