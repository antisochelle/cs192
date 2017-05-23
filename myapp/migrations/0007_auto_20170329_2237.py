# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-29 14:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20170329_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='misconducts',
            name='csc_section',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='misconducts',
            name='csc_version',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='misconducts',
            name='for_student',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='misconducts',
            name='misconduct_general',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='misconducts',
            name='misconduct_specific',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='respondents',
            name='degree_program',
            field=models.TextField(blank=True, default='None'),
        ),
    ]
