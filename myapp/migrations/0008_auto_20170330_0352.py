# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-29 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20170329_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='case_number',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='misconducts',
            name='for_student',
            field=models.BooleanField(default=1),
        ),
    ]
