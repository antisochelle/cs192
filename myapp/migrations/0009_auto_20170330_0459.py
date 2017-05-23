# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-29 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20170330_0352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audit_trail',
            name='case_id',
        ),
        migrations.AddField(
            model_name='audit_trail',
            name='action',
            field=models.TextField(default='Logged in'),
        ),
        migrations.AddField(
            model_name='audit_trail',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.Users'),
            preserve_default=False,
        ),
    ]