# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-29 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20170329_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audit_trail',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
