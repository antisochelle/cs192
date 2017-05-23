# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-17 20:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20170411_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ahdhc_members',
            name='first_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ahdhc_members',
            name='last_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='adhdc_constitution_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='ahdhc_constitution_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='ahdhc_orientation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='ahdhc_preliminary_deliberation_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='appeal_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='case_number',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='case_resolution_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='decision_copy_to_chancellor_date',
            field=models.DateField(blank=True, db_column='decision_copy to_chancellor_date', null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='decision_copy_to_chancellor_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='decision_issuance_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='decision_issuance_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='decision_receipt_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='final_committee_report_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='final_committee_report_receipt_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='preliminary_meeting_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='preliminary_meeting_notice_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='preliminary_meeting_report_date_filed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='respondednt_answer_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='respondent_answer_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='summons_issuance_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='summons_issuance_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='summons_receipt_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='summons_receipt_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='summons_service_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases',
            name='summons_service_deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cases_misconducts_respondents',
            name='corrective_measure',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='misconducts',
            name='csc_section',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='misconducts',
            name='csc_version',
            field=models.TextField(blank=True, null=True),
        ),
    ]