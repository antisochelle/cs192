# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-29 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20170329_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respondents',
            name='degree_program',
            field=models.TextField(blank=True, null=True),
        ),
    ]
