# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `#managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        #managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        #managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=150)

    class Meta:
        #managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        #managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


# SDC_DATABASE MODELS

class Cases(models.Model):
    case_id = models.IntegerField(primary_key=True)  # This field type is a guess. /
    complaint_date_received = models.DateField()
    complaint_sdc_receipt_deadline = models.DateField()
    initial_report_deadline = models.DateField()
    initial_report_release_date = models.DateField()
    jurisdiction = models.IntegerField()  # This field type is a guess./
    is_adr_ok = models.BooleanField(default=1)  # This field type is a guess./
    adr_deadline = models.DateField()
    did_adr_work = models.BooleanField(default=1)  # This field type is a guess./
    case_number = models.TextField(max_length=100, blank=True, null=True)
    ahdhc_constitution_deadline = models.DateField(blank=True, null=True)
    ahdhc_constitution_date = models.DateField(blank=True, null=True)
    ahdhc_orientation_date = models.DateField(blank=True, null=True)
    summons_issuance_deadline = models.DateField(blank=True, null=True)
    summons_issuance_date = models.DateField(blank=True, null=True)
    summons_service_deadline = models.DateField(blank=True, null=True)
    summons_service_date = models.DateField(blank=True, null=True)
    summons_receipt_deadline = models.DateField(blank=True, null=True)
    summons_receipt_date = models.DateField(blank=True, null=True)
    respondent_answer_deadline = models.DateField(blank=True, null=True)
    respondent_answer_date = models.DateField(blank=True, null=True)
    ahdhc_preliminary_deliberation_date = models.DateField(blank=True, null=True)
    preliminary_meeting_notice_deadline = models.DateField(blank=True, null=True)
    preliminary_meeting_date = models.DateField(blank=True, null=True)
    preliminary_meeting_report_done = models.BooleanField(default=0)  # This field type is a guess./
    preliminary_meeting_report_date_filed = models.DateField(blank=True, null=True)
    case_resolution_deadline = models.DateField(blank=True, null=True)
    final_committee_report_deadline = models.DateField(blank=True, null=True)
    final_committee_report_receipt_date = models.DateField(blank=True, null=True)
    decision_issuance_deadline = models.DateField(blank=True, null=True)
    decision_issuance_date = models.DateField(blank=True, null=True)
    decision_copy_to_chancellor_deadline = models.DateField(blank=True, null=True)
    decision_copy_to_chancellor_date = models.DateField(db_column='decision_copy to_chancellor_date', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    decision_receipt_date = models.DateField(blank=True, null=True)
    appeal_deadline = models.DateField(blank=True, null=True)
    appeal_made = models.BooleanField(default=0)  # This field type is a guess./
    case_closed = models.BooleanField(default=0)  # This field type is a guess./

    class Meta:
        #managed = False
        db_table = 'cases'

class College(models.Model):
    college_id = models.IntegerField(primary_key=True)  # This field type is a guess./
    name = models.TextField()

    class Meta:
        #managed = False
        db_table = 'college'

# Unable to inspect table 'department'/
# The error was: 'NoneType' object has no attribute 'groups'/

class Department(models.Model):
    department_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    college_id = models.ForeignKey(College, db_column='college_id', on_delete=models.CASCADE)

    class Meta:
        #managed = False
        db_table = 'department'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        #managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'django_session'


class Misconduct(models.Model):
    misconduct_id = models.IntegerField(primary_key=True)  # This field type is a guess./
    csc_section = models.TextField(max_length=100, blank=True, null=True)
    misconduct_general = models.CharField(max_length=100, blank=True)
    misconduct_specific = models.TextField(blank=True)
    for_student = models.BooleanField(default=1) #CHANGED FROM TEXT FIELD TO BOOLEAN
    is_serious = models.BooleanField(default=1)  # This field type is a guess.
    csc_version = models.TextField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'misconducts'

class Respondent(models.Model):
    respondent_id = models.IntegerField(primary_key=True)
    last_name = models.TextField()
    first_name = models.TextField()
    middle_name = models.TextField()
    degree_program = models.TextField(blank=True, default='None')
    department_id = models.ForeignKey(Department, db_column='department_id', on_delete=models.CASCADE)
    is_student = models.BooleanField(default=1)

    class Meta:
        #managed = False
        db_table = 'respondents'

class univ_rep(models.Model):
    rep_id = models.IntegerField(primary_key=True)
    last_name = models.TextField()
    first_name = models.TextField()
    department_id = models.ForeignKey(Department, db_column='department_id', on_delete=models.CASCADE)

    class Meta:
        #managed = False
        db_table = 'univ_reps'


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.TextField(max_length=100)
    role_id = models.IntegerField() 
    password = models.CharField(max_length=128)

    class Meta:
        #managed = False
        db_table = 'users'


class UsersRole(models.Model):
    id = models.IntegerField(primary_key=True) 
    role_name = models.TextField()

    class Meta:
        #managed = False
        db_table = 'users_role'



# WITH FOREIGN KEY

class ahdhc_members(models.Model):
    member_id = models.IntegerField(primary_key=True)
    last_name = models.TextField(blank=True, null=True)
    first_name = models.TextField(blank=True, null=True)
    department_id = models.ForeignKey(Department, db_column='department_id', on_delete=models.CASCADE)
    is_student = models.BooleanField(default=1)

    class Meta:
        db_table = 'ahdhc_members'


class audit_trail(models.Model):
    id = models.AutoField(primary_key=True)
    entry_date = models.DateTimeField()
    user_id = models.ForeignKey(Users, db_column='user_id', on_delete=models.CASCADE)
    action = models.TextField(default='Logged in')

    class Meta:
        db_table = 'audit_trail'

class cases_ahdhc_members(models.Model):
    id = models.AutoField(primary_key=True)
    case_id = models.ForeignKey(Cases, db_column='case_id', on_delete=models.CASCADE)
    member_id = models.ForeignKey(ahdhc_members, db_column='member_id', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cases_ahdhc_members'


class cases_hearings(models.Model):
    id = models.AutoField(primary_key=True)
    case_id = models.ForeignKey(Cases, db_column='case_id', on_delete=models.CASCADE)
    hearing_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'cases_hearings'


class cases_misconducts_respondents(models.Model):
    id = models.AutoField(primary_key=True)
    case_id = models.ForeignKey(Cases, db_column='case_id', on_delete=models.CASCADE)
    misconduct_id = models.ForeignKey(Misconduct, db_column='misconduct_id', on_delete=models.CASCADE)
    misconduct_details = models.TextField()
    respondent_id = models.ForeignKey(Respondent, db_column='respondent_id', on_delete=models.CASCADE)
    is_guilty = models.BooleanField(default=0)
    corrective_measure = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'cases_misconducts_respondents'


class Announcements(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
    date_posted = models.DateField()

    class Meta:
        db_table = 'announcements'