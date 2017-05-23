import datetime
import hashlib
from django.utils import timezone
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from .models import Users, UsersRole, Cases, cases_misconducts_respondents, Misconduct, Respondent, Announcements, Department, audit_trail, College, univ_rep, ahdhc_members, cases_ahdhc_members, cases_hearings    # Importing the classes
from django.contrib import messages

session_user_id = "None"
login = 0
acc_type = "None"

# Create your views here.
def index(request):
	return render_to_response('index.html')


def login_view(request):
	if login == 0:
		if request.method == "POST":
			global login
			global acc_type
			global session_user_id
			role_id = 0

			username = request.POST['username']
			password = request.POST['password']
			acc_type = request.POST['acc_type']

			# hash password
			password = hashlib.md5(password.encode()).hexdigest()
			
			if acc_type == "Admin": role_id = 1
			elif acc_type == "Chair": role_id = 2
			elif acc_type == "Staff": role_id = 3
			elif acc_type == "Member": role_id = 4

			username_valid = Users.objects.filter(username = username)
			password_valid = Users.objects.filter(username = username, password = password)
			type_valid = Users.objects.filter(username = username, password = password, role_id = role_id)
			
			if not username_valid:
				messages.error(request, 'User does not exist')
			elif not password_valid:
				messages.error(request, 'Invalid password')
			elif not type_valid:
				messages.error(request, 'Invalid account type')
			else:
				if (acc_type != "Admin" and acc_type != "Chair" and acc_type != "Staff" and acc_type != "Member"):
					messages.error(request, 'Please select account type.')
					return render(request, "index.html")

				login = 1
				session_user_id = type_valid[0].user_id

				# add to audit trail
				action = ' logged in'
				add_to_trail(action)

				return HttpResponseRedirect("/home")

		return render(request, "index.html")
	return HttpResponseRedirect("/home")


def home(request):
	global session_user_id
	if login == 1:
		queryset = Announcements.objects.all().order_by('-id')[:5]	# create list of announcements

		# get list of deadlines for Dashboard Calendar from cases_misconducts_respondents table
		cases = cases_misconducts_respondents.objects.all()

		context = {
			"queryset": queryset, 
			"cmr": cases
		}

		if acc_type == "Admin": return render(request, 'admin_dashboard.html', context)
		elif acc_type == "Chair": return render(request, 'chair_dashboard.html', context)
		elif acc_type == "Staff": return render(request, 'staff_dashboard.html', context)
		elif acc_type == "Member": return render(request, 'member_dashboard.html', context)

	return HttpResponseRedirect("/login")

def cases(request):
	if login == 1:
		# code for showing all cases
		queryset = Cases.objects.all()	# create list of cases 
		
		context = {
			"queryset": queryset
		}

		if acc_type == "Chair":
			return render(request, 'cases_chair.html', context)
		elif acc_type == "Member":
			return render(request, 'cases_without_edit_delete.html', context)
		else:
			return render(request, 'cases.html', context)
	return HttpResponseRedirect("/login")


def add_announcement(request):
	if login == 1: 

		context = {
			"user_id": session_user_id
		}		

		if acc_type == "Admin":
			return render(request, 'add_announcement_with_view_users.html', context)
		elif acc_type == "Chair":
			return render(request, 'chair_add_announcement.html', context)
		elif acc_type == "Staff":
			return render(request, 'staff_add_announcement.html', context)
		elif acc_type == "Member":
			return render(request, 'member_add_announcement.html', context)
	return HttpResponseRedirect("/login")


def announcement_success(request):
	if login == 1:
		if request.method == "POST":
			passed_title = request.POST['title']
			passed_desc = request.POST['desc']
			# passed_date = request.POST['date']

			# get id of last announcement in the table
			queryset = Announcements.objects.all()	# get list of announcements
			if len(queryset) != 0:
				last_id = queryset[len(queryset)-1].id  # get last id in the announcement list
			else:
				last_id = 0

			new_announcement = Announcements(id=last_id+1, title=passed_title, description=passed_desc, date_posted=datetime.datetime.now())
			new_announcement.save()

			# add to audit trail
			action = ' added announcement'
			add_to_trail(action)

		return HttpResponseRedirect("/home")
	return HttpResponseRedirect("/login")


def logout(request):
	if login == 1:
		global login
		global acc_type

		login = 0
		acc_type = "None"

		# add to audit trail
		action = ' logged out'
		add_to_trail(action)

		return HttpResponseRedirect('/login')
	return HttpResponseRedirect("/login")

# view individual case details
def view_case(request):
	if login == 1:
		passed_case_id = request.GET['passed_case_id']	# passed_case_id is the value of case_id from /cases

		if not passed_case_id:
			if acc_type == "Member":
				return render(request, 'cases_without_edit_delete.html')
			else:
				return render(request, 'cases.html')

		else:
			queryset = Cases.objects.filter(case_id = passed_case_id)	# get specific case using case_id 
			
			# get respondent & misconduct for this case
			cmr = cases_misconducts_respondents.objects.filter(case_id = passed_case_id)
			members = cases_ahdhc_members.objects.filter(case_id = passed_case_id)
			context = {
				"queryset": queryset,
				"cmr": cmr,
				"contents": len(cmr),
				"members": members
			}

			# add to audit trail
			action = ' viewed all cases'
			add_to_trail(action)

			if acc_type == "Chair":
				return render(request, "chair_view_case.html", context)
			elif acc_type == "Member":
				return render(request, "member_view_case.html", context)
			elif acc_type == "Staff":
				return render(request, 'staff_view_case.html', context)
			else:
				return render(request, "view_case.html", context)
	return HttpResponseRedirect("/login")

def edit_case(request):
	if login == 1:
		passed_case_id = request.GET['passed_case_id']	# passed_case_id is the value of case_id from /cases

		if not passed_case_id:
			if acc_type == "Chair":
				return render(request, 'cases_chair.html')
			elif acc_type == "Member":
				return render(request, 'cases_without_edit_delete.html')
			else:
				return render(request, 'cases.html')

		else:
			queryset = Cases.objects.filter(case_id = passed_case_id)	# get specific case using case_id 
			departments = Department.objects.all()
			misconducts = Misconduct.objects.all()
			members = ahdhc_members.objects.all()
			hearings = cases_hearings.objects.filter(case_id = passed_case_id)
			context = {
				"queryset": queryset,
				"departments": departments,
				"misconducts": misconducts,
				"members": members,
				"hearings": hearings
			}

			if acc_type == "Chair":
				return render(request, "chair_edit_case.html", context)
			else:
				return render(request, "edit_case.html", context)
	return HttpResponseRedirect("/login")

def delete_case(request):
	if login == 1:
		if request.method == "POST":
			passed_case_id = request.POST['case_id']
			delete_case = Cases.objects.filter(case_id = passed_case_id)

			# add to audit trail
			action = ' deleted case ' + delete_case[0].case_number
			add_to_trail(action)

			# delete
			delete_case.delete()
		
		return HttpResponseRedirect("/cases/")

def add_case(request):
	if login == 1: 
			
		departments = Department.objects.all()
		misconducts = Misconduct.objects.all()
		members = ahdhc_members.objects.all()
		context = {
			"departments": departments,
			"misconducts": misconducts,
			"members": members
		}

		if acc_type == "Chair":
			return render(request, 'chair_add_case.html', context)
		elif acc_type == "Staff":
			return render(request, 'staff_add_case.html', context)
	return HttpResponseRedirect("/login")

def case_success(request):
	if login == 1:
		if request.method == "POST":

			# Values for Respondent
			passed_respondent_first_name = request.POST['respondent_first_name']
			passed_respondent_middle_name = request.POST['respondent_middle_name']
			passed_respondent_last_name = request.POST['respondent_last_name']
			passed_department_name = request.POST['department_name']

			# Values for Misconduct
			passed_misconduct = request.POST['misconduct_name']

			# Values for Cases
			passed_case_number = request.POST['case_number']
			passed_complaint_received_date = request.POST['complaint_received_date']
			passed_complaint_receipt_deadline = request.POST['complaint_receipt_deadline']
			passed_init_report_deadline = request.POST['init_report_deadline']
			passed_init_report_release_date = request.POST['init_report_release_date']
			passed_jurisdiction_num = request.POST['jurisdiction_num']
			passed_adr_status = request.POST['adr_status']
			if passed_adr_status == "Yes":
				passed_adr_status = True
			elif passed_adr_status == "No":
				passed_adr_status = False
			passed_adr_deadline = request.POST['adr_deadline']
			passed_adr_work_status = request.POST['adr_work_status']
			if passed_adr_work_status == "Yes":
				passed_adr_work_status = True
			elif passed_adr_work_status == "No":
				passed_adr_work_status = False
			passed_consti_deadline = request.POST['consti_deadline'] or None
			passed_consti_date = request.POST['consti_date'] or None
			passed_orie_date = request.POST['orie_date'] or None
			passed_issuance_deadline = request.POST['issuance_deadline'] or None
			passed_issuance_date = request.POST['issuance_date'] or None
			passed_service_deadline = request.POST['service_deadline'] or None
			passed_service_date = request.POST['service_date'] or None
			passed_receipt_deadline = request.POST['receipt_deadline'] or None
			passed_receipt_date = request.POST['receipt_date'] or None
			passed_answer_deadline = request.POST['answer_deadline'] or None
			passed_answer_date = request.POST['answer_date'] or None
			passed_prelim_delib_date = request.POST['prelim_delib_date'] or None
			passed_meeting_notice_deadline = request.POST['meeting_notice_deadline'] or None
			passed_meeting_date = request.POST['meeting_date'] or None
			passed_meeting_report_status = request.POST['meeting_report_status']
			if passed_meeting_report_status == "Yes":
				passed_meeting_report_status = True
			elif passed_meeting_report_status == "No":
				passed_meeting_report_status = False
			passed_meeting_report_file_date = request.POST['meeting_report_file_date'] or None
			passed_resolution_deadline = request.POST['resolution_deadline'] or None
			passed_final_report_deadline = request.POST['final_report_deadline'] or None
			passed_final_report_receipt_date = request.POST['final_report_receipt_date'] or None
			passed_decision_deadline = request.POST['decision_deadline'] or None
			passed_decision_date = request.POST['decision_date'] or None
			passed_decision_chancellor_deadline = request.POST['decision_chancellor_deadline'] or None
			passed_decision_chancellor_date = request.POST['decision_chancellor_date'] or None
			passed_decision_receipt_date = request.POST['decision_receipt_date'] or None
			passed_appeal_deadline = request.POST['appeal_deadline'] or None
			passed_appeal_status = request.POST['appeal_status']
			if passed_appeal_status == "Yes":
				passed_appeal_status = True
			elif passed_appeal_status == "No":
				passed_appeal_status = False
			passed_case_status = request.POST['case_status']
			if passed_case_status == "Yes":
				passed_case_status = True
			else:
				passed_case_status = False

			# Case
			# get id of last case in the table
			queryset = Cases.objects.all()	
			if len(queryset) != 0:
				case_last_id = queryset[len(queryset)-1].case_id
			else:
				case_last_id = 0

			new_case = Cases(case_id=case_last_id+1, 
							complaint_date_received = passed_complaint_received_date, 
							complaint_sdc_receipt_deadline = passed_complaint_receipt_deadline,
							initial_report_deadline = passed_init_report_deadline,
							initial_report_release_date = passed_init_report_release_date,
							jurisdiction = passed_jurisdiction_num,
							is_adr_ok = passed_adr_status,
							adr_deadline = passed_adr_deadline,
							did_adr_work = passed_adr_work_status,
							case_number = passed_case_number,
							ahdhc_constitution_deadline = passed_consti_deadline,
							ahdhc_constitution_date = passed_consti_date,
							ahdhc_orientation_date = passed_orie_date,
							summons_issuance_deadline = passed_issuance_deadline,
							summons_issuance_date = passed_issuance_date,
							summons_service_deadline = passed_service_deadline,
							summons_service_date = passed_service_date,
							summons_receipt_deadline = passed_receipt_deadline,
							summons_receipt_date = passed_receipt_date,
							respondent_answer_deadline = passed_answer_deadline,
							respondent_answer_date = passed_answer_date,
							ahdhc_preliminary_deliberation_date = passed_prelim_delib_date,
							preliminary_meeting_notice_deadline = passed_meeting_notice_deadline,
							preliminary_meeting_date = passed_meeting_date,
							preliminary_meeting_report_done = passed_meeting_report_status,
							preliminary_meeting_report_date_filed = passed_meeting_report_file_date,
							case_resolution_deadline = passed_resolution_deadline,
							final_committee_report_deadline = passed_final_report_deadline,
							final_committee_report_receipt_date = passed_final_report_receipt_date,
							decision_issuance_deadline = passed_decision_deadline,
							decision_issuance_date = passed_decision_date,
							decision_copy_to_chancellor_deadline = passed_decision_chancellor_deadline,
							decision_copy_to_chancellor_date = passed_decision_chancellor_date,
							decision_receipt_date = passed_decision_receipt_date,
							appeal_deadline = passed_appeal_deadline,
							appeal_made = passed_appeal_status,
							case_closed = passed_case_status)
			new_case.save()

			# Respondent
			queryset = Respondent.objects.all() # get id of last respondent in the table
			if len(queryset) != 0:
				resp_last_id = queryset[len(queryset)-1].respondent_id+1
			else:
				resp_last_id = 1

			get_department = Department.objects.filter(name=passed_department_name)
			new_respondent = Respondent(respondent_id = resp_last_id,
			    last_name = passed_respondent_last_name,
			    first_name = passed_respondent_first_name,
			    middle_name = passed_respondent_middle_name,
			    department_id = get_department[0])
			new_respondent.save()

			# cases_misconducts_respondents
			get_case = Cases.objects.filter(case_id=case_last_id+1)
			get_misconduct = Misconduct.objects.filter(misconduct_general=passed_misconduct)
			get_respondent = Respondent.objects.filter(respondent_id=resp_last_id)
			new_cmr = cases_misconducts_respondents(case_id = get_case[0],
				misconduct_id = get_misconduct[0],
				misconduct_details = get_misconduct[0].misconduct_general,
				respondent_id = get_respondent[0])
			new_cmr.save()

			# add to audit trail
			action = ' added new case: ' + new_case.case_number 
			add_to_trail(action)


		return HttpResponseRedirect("/cases/")
	return HttpResponseRedirect("/login")

def edit_case_success(request):
	if login == 1:
		if request.method == "POST":

			# Values for cases_misconducts_respondents
			passed_is_guilty = request.POST['is_guilty']
			if passed_is_guilty == "Yes":
				passed_is_guilty = True
			elif passed_is_guilty == "No":
				passed_is_guilty = False
			passed_corrective_measure = request.POST['corrective_measure']
			
			# Values for cases_hearings
			passed_hearing_date = request.POST['hearing_date']

			# Values for AHDHC Members
			passed_member = request.POST['hearing_member']

			# Values for Cases
			passed_case_number = request.POST['case_number']
			passed_complaint_received_date = request.POST['complaint_received_date'] or None
			passed_complaint_receipt_deadline = request.POST['complaint_receipt_deadline'] or None
			passed_init_report_deadline = request.POST['init_report_deadline'] or None
			passed_init_report_release_date = request.POST['init_report_release_date'] or None
			passed_jurisdiction_num = request.POST['jurisdiction_num']
			passed_adr_status = request.POST['adr_status']
			if passed_adr_status == "Yes":
				passed_adr_status = True
			elif passed_adr_status == "No":
				passed_adr_status = False
			passed_adr_deadline = request.POST['adr_deadline'] or None
			passed_adr_work_status = request.POST['adr_work_status']
			if passed_adr_work_status == "Yes":
				passed_adr_work_status = True
			elif passed_adr_work_status == "No":
				passed_adr_work_status = False
			passed_consti_deadline = request.POST['consti_deadline'] or None
			passed_consti_date = request.POST['consti_date'] or None
			passed_orie_date = request.POST['orie_date'] or None
			passed_issuance_deadline = request.POST['issuance_deadline'] or None
			passed_issuance_date = request.POST['issuance_date'] or None
			passed_service_deadline = request.POST['service_deadline'] or None
			passed_service_date = request.POST['service_date'] or None
			passed_receipt_deadline = request.POST['receipt_deadline'] or None
			passed_receipt_date = request.POST['receipt_date'] or None
			passed_answer_deadline = request.POST['answer_deadline'] or None
			passed_answer_date = request.POST['answer_date'] or None
			passed_prelim_delib_date = request.POST['prelim_delib_date'] or None
			passed_meeting_notice_deadline = request.POST['meeting_notice_deadline'] or None
			passed_meeting_date = request.POST['meeting_date'] or None
			passed_meeting_report_status = request.POST['meeting_report_status']
			if passed_meeting_report_status == "Yes":
				passed_meeting_report_status = True
			elif passed_meeting_report_status == "No":
				passed_meeting_report_status = False
			passed_meeting_report_file_date = request.POST['meeting_report_file_date'] or None
			passed_resolution_deadline = request.POST['resolution_deadline'] or None
			passed_final_report_deadline = request.POST['final_report_deadline'] or None
			passed_final_report_receipt_date = request.POST['final_report_receipt_date'] or None
			passed_decision_deadline = request.POST['decision_deadline'] or None
			passed_decision_date = request.POST['decision_date'] or None
			passed_decision_chancellor_deadline = request.POST['decision_chancellor_deadline'] or None
			passed_decision_chancellor_date = request.POST['decision_chancellor_date'] or None
			passed_decision_receipt_date = request.POST['decision_receipt_date'] or None
			passed_appeal_deadline = request.POST['appeal_deadline'] or None
			passed_appeal_status = request.POST['appeal_status']
			if passed_appeal_status == "Yes":
				passed_appeal_status = True
			elif passed_appeal_status == "No":
				passed_appeal_status = False
			passed_case_status = request.POST['case_status']
			if passed_case_status == "Yes":
				passed_case_status = True
			elif passed_case_status == "No":
				passed_case_status = False

			# get id from form
			passed_case_id = request.POST['case_id']
			Cases.objects.filter(case_id=passed_case_id).update(case_number=passed_case_number,
							complaint_date_received = passed_complaint_received_date, 
							complaint_sdc_receipt_deadline = passed_complaint_receipt_deadline,
							initial_report_deadline = passed_init_report_deadline,
							initial_report_release_date = passed_init_report_release_date,
							jurisdiction = passed_jurisdiction_num,
							is_adr_ok = passed_adr_status,
							adr_deadline = passed_adr_deadline,
							did_adr_work = passed_adr_work_status,
							ahdhc_constitution_deadline = passed_consti_deadline,
							ahdhc_constitution_date = passed_consti_date,
							ahdhc_orientation_date = passed_orie_date,
							summons_issuance_deadline = passed_issuance_deadline,
							summons_issuance_date = passed_issuance_date,
							summons_service_deadline = passed_service_deadline,
							summons_service_date = passed_service_date,
							summons_receipt_deadline = passed_receipt_deadline,
							summons_receipt_date = passed_receipt_date,
							respondent_answer_deadline = passed_answer_deadline,
							respondent_answer_date = passed_answer_date,
							ahdhc_preliminary_deliberation_date = passed_prelim_delib_date,
							preliminary_meeting_notice_deadline = passed_meeting_notice_deadline,
							preliminary_meeting_date = passed_meeting_date,
							preliminary_meeting_report_done = passed_meeting_report_status,
							preliminary_meeting_report_date_filed = passed_meeting_report_file_date,
							case_resolution_deadline = passed_resolution_deadline,
							final_committee_report_deadline = passed_final_report_deadline,
							final_committee_report_receipt_date = passed_final_report_receipt_date,
							decision_issuance_deadline = passed_decision_deadline,
							decision_issuance_date = passed_decision_date,
							decision_copy_to_chancellor_deadline = passed_decision_chancellor_deadline,
							decision_copy_to_chancellor_date = passed_decision_chancellor_date,
							decision_receipt_date = passed_decision_receipt_date,
							appeal_deadline = passed_appeal_deadline,
							appeal_made = passed_appeal_status,
							case_closed = passed_case_status)

			# cases_misconducts_respondents
			cases_misconducts_respondents.objects.filter(case_id=passed_case_id).update(is_guilty=passed_is_guilty, corrective_measure=passed_corrective_measure)
			
			# cases_ahdhc_members
			get_case = Cases.objects.filter(case_id=passed_case_id)
			get_member = ahdhc_members.objects.filter(last_name=passed_member)
			check = cases_ahdhc_members.objects.filter(case_id=get_case[0])
			if len(check) == 0:
				new_cam = cases_ahdhc_members(case_id=get_case[0], member_id=get_member[0])
				new_cam.save()

			# cases_hearings
			check = cases_hearings.objects.filter(case_id=get_case[0])
			if passed_hearing_date == '': 
				passed_hearing_date = None
			if len(check) == 0 and passed_hearing_date != None:
				new_hearing = cases_hearings(case_id=get_case[0], hearing_date=passed_hearing_date)
				new_hearing.save()
			else:
				cases_hearings.objects.filter(case_id=get_case[0].case_id).update(hearing_date=passed_hearing_date)

			# add to audit trail
			get_case = Cases.objects.filter(case_id=passed_case_id)
			action = ' edited case ' + get_case[0].case_number
			add_to_trail(action)

		return HttpResponseRedirect("/cases/")
	return HttpResponseRedirect("/login")

def users(request):
	if login == 1:
		# code for showing all Users
		queryset = Users.objects.all().order_by('role_id')
		
		context = {
			"queryset": queryset
		}

		return render(request, 'users.html', context)
	return HttpResponseRedirect("/login")

def add_user(request):
	if login == 1 and acc_type == "Admin":
		return render(request, 'add_user.html')
	return HttpResponseRedirect("/login")

def view_user(request):
	if login == 1:
		passed_user_id = request.GET['passed_user_id']
		print(passed_user_id)
		if not passed_user_id:
			return render(request, 'users.html')

		else:
			queryset = Users.objects.filter(user_id = passed_user_id)	# get specific user using user_id 
			context = {
				"queryset": queryset
			}

		return render(request, "view_user.html", context)
		
	return HttpResponseRedirect("/login")

def edit_user(request):
	if login == 1:
		passed_user_id = request.GET['passed_user_id']	# passed_user_id is the value of user_id from /users

		if not passed_user_id:
			return render(request, 'users.html')

		else:
			queryset = Users.objects.filter(user_id = passed_user_id)	# get specific case using case_id 
			context = {
				"queryset": queryset
			}

			return render(request, "edit_user.html", context)
	return HttpResponseRedirect("/login")

def edit_user_success(request):
	if login == 1:
		if request.method == "POST":
			passed_username = request.POST['username']
			passed_role_id = request.POST['role_id']
			
			# get id from form
			passed_user_id = request.POST['user_id']

			Users.objects.filter(user_id=passed_user_id).update(
							user_id = passed_user_id, 
							username = passed_username,
							role_id = passed_role_id,
							)

			get_user = Users.objects.filter(user_id=passed_user_id)

			# add to audit trail
			action = ' edited user ' + get_user[0].username
			add_to_trail(action)

		return HttpResponseRedirect("/users/")
	return HttpResponseRedirect("/login")

def delete_user(request):
	if login == 1:
		if request.method == "POST":
			passed_user_id = request.POST['user_id']

			if session_user_id != passed_user_id:
				delete_user = Users.objects.filter(user_id = passed_user_id)

				# add to audit trail
				action = ' deleted user ' + delete_user[0].username
				add_to_trail(action)

				# delete
				delete_user.delete()
		
		return HttpResponseRedirect("/users/")
	return HttpResponseRedirect("/login")

def user_success(request):
	if login == 1:
		if request.method == "POST":
			passed_username = request.POST['username']
			passed_role_id = request.POST['role_id']
			passed_password = request.POST['password']

			# get last id in table
			queryset = Users.objects.all()	# get list of users
			if len(queryset) != 0:
				last_id = queryset[len(queryset)-1].user_id  # get last id 
			else:
				last_id = 0

			# hash the password
			hash_password = hashlib.md5(passed_password.encode())

			new_user = Users(user_id=last_id+1, username=passed_username, role_id=passed_role_id, password=hash_password.hexdigest())
	
			new_user.save()

			# add to audit trail
			action = ' added user ' + new_user.username
			add_to_trail(action)

		return HttpResponseRedirect("/users/")
	return HttpResponseRedirect("/login")

def misconducts(request):
	if login == 1:
		# code for showing all Misconduct
		queryset = Misconduct.objects.all()
		
		context = {
			"queryset": queryset
		}

		if acc_type == "Admin":
			return render(request, 'admin_misconducts.html', context)
		elif acc_type == "Chair":
			return render(request, 'chair_misconducts.html', context)
	return HttpResponseRedirect("/login")

def view_misconduct(request):
	if login == 1:
		passed_misconduct_id = request.GET['passed_misconduct_id']

		if not passed_misconduct_id:
			if acc_type == "Admin":
				return render(request, 'admin_misconducts.html', context)
			elif acc_type == "Chair":
				return render(request, 'chair_misconducts.html', context)
		else:
			queryset = Misconduct.objects.filter(misconduct_id = passed_misconduct_id)
			context = {
				"queryset": queryset
			}

		if acc_type == "Admin":
			return render(request, 'admin_view_misconduct.html', context)
		elif acc_type == "Chair":
			return render(request, 'chair_view_misconduct.html', context)
		
	return HttpResponseRedirect("/login")

def edit_misconduct(request):
	if login == 1 and acc_type != "Member" and acc_type != "Staff":
		passed_misconduct_id = request.GET['passed_misconduct_id']

		if not passed_misconduct_id:
			if acc_type == "Admin":
				return render(request, 'admin_misconducts.html', context)
			elif acc_type == "Chair":
				return render(request, 'chair_misconducts.html', context)

		else:
			queryset = Misconduct.objects.filter(misconduct_id = passed_misconduct_id)
			context = {
				"queryset": queryset
			}

			# add to audit trail
			action = ' edited misconduct ' + queryset[0].misconduct_general
			add_to_trail(action)

			if acc_type == "Admin":
				return render(request, 'admin_edit_misconduct.html', context)
			elif acc_type == "Chair":
				return render(request, 'chair_edit_misconduct.html', context)
	return HttpResponseRedirect("/login")

def edit_misconduct_success(request):

	if login == 1:
		if request.method == "POST":
			passed_misconduct_id = request.POST['misconduct_id']
			passed_csc_section = request.POST['csc_section']
			
			# get id from form
			passed_misconduct_general = request.POST['misconduct_general']
			passed_misconduct_specific = request.POST['misconduct_specific']
			passed_for_student = request.POST['for_student']
			if passed_for_student == "Yes":
				passed_for_student = True
			elif passed_for_student == "No":
				passed_for_student = False
			passed_is_serious = request.POST['is_serious']
			if passed_is_serious == "Yes":
				passed_is_serious = True
			elif passed_is_serious == "No":
				passed_is_serious = False
			passed_csc_version = request.POST['csc_version']

			Misconduct.objects.filter(misconduct_id=passed_misconduct_id).update(
							misconduct_id = passed_misconduct_id, 
							csc_section = passed_csc_section,
							misconduct_general = passed_misconduct_general,
							misconduct_specific = passed_misconduct_specific,
							for_student = passed_for_student,
							is_serious = passed_is_serious,
							csc_version = passed_csc_version,
							)

			get_misconduct = Misconduct.objects.filter(misconduct_id=passed_misconduct_id)

			# add to audit trail
			action = ' edited misconduct ' + get_misconduct[0].misconduct_general
			add_to_trail(action)

		return HttpResponseRedirect("/misconducts/")
	return HttpResponseRedirect("/login")

def delete_misconduct(request):
	if login == 1:
		if request.method == "POST":
			passed_misconduct_id = request.POST['misconduct_id']
			delete_misconduct = Misconduct.objects.filter(misconduct_id = passed_misconduct_id)

			# # add to audit trail
			action = ' deleted misconduct ' + delete_misconduct[0].misconduct_general
			add_to_trail(action)

			# delete
			delete_misconduct.delete()
		
		return HttpResponseRedirect("/misconducts/")
	return HttpResponseRedirect("/login")

def add_misconduct(request):
	if login == 1:
		if acc_type == "Admin":
			return render(request, 'admin_add_misconduct.html')
		elif acc_type == "Chair":
			return render(request, 'chair_add_misconduct.html')
	return HttpResponseRedirect("/login")

def add_misconduct_success(request):
	if login == 1:
		if request.method == "POST":
			passed_csc_section = request.POST['csc_section']
			passed_misconduct_general = request.POST['misconduct_general']
			passed_misconduct_specific = request.POST['misconduct_specific']
			passed_for_student = request.POST['for_student']
			if passed_for_student == "Yes":
				passed_for_student = True
			elif passed_for_student == "No":
				passed_for_student = False
			passed_is_serious = request.POST['is_serious']
			if passed_is_serious == "Yes":
				passed_is_serious = True
			elif passed_is_serious == "No":
				passed_is_serious = False
			passed_csc_version = request.POST['csc_version']

			# get id of last college in table
			queryset = Misconduct.objects.all()	# get list of colleges
			if len(queryset) != 0:
				last_id = queryset[len(queryset)-1].misconduct_id  # get last id 
			else:
				last_id = 0

			new_misconduct = Misconduct(misconduct_id=last_id + 1, csc_section=passed_csc_section,
								         misconduct_general=passed_misconduct_general, misconduct_specific=passed_misconduct_specific,
								         for_student=passed_for_student, is_serious=passed_is_serious, csc_version=passed_csc_version)
			new_misconduct.save()

			# add to audit trail
			action = ' added misconduct ' + new_misconduct.misconduct_general
			add_to_trail(action)

		return HttpResponseRedirect("/misconducts/")
	return HttpResponseRedirect("/login")

# view audit trail
def view_trail(request):
	if login == 1:
		queryset = audit_trail.objects.all().order_by('-entry_date')[:10]	# create list of logs
		context = {
			"queryset": queryset,
			"user_id": session_user_id
		}		

		if acc_type == "Admin":
			return render(request, "admin_audit_trail.html", context)
		elif acc_type == "Chair":
			return render(request, "chair_audit_trail.html", context)

	return HttpResponseRedirect("/login")

# adding to audit trail
def add_to_trail(action):
	# action is the activity, passed

	# add to audit trail
	session_user = Users.objects.filter(user_id = session_user_id)
	if len(session_user) != 0:
		get_action = session_user[0].username + action

	new_log = audit_trail(entry_date=datetime.datetime.now(), 
		user_id=session_user[0], 
		action=get_action)

	new_log.save()

def colleges(request):
	if login == 1:

		# code for showing all Colleges
		queryset = College.objects.all() 
		
		context = {
			"queryset": queryset
		}

		# add to audit trail
		action = ' viewed all colleges'
		add_to_trail(action)

		if acc_type == "Admin":
			return render(request, 'admin_colleges.html', context)
		elif acc_type == "Chair":
			return render(request, 'chair_colleges.html', context)
	return HttpResponseRedirect("/login")

def edit_college(request):
	if login == 1 and acc_type != "Member" and acc_type != "Staff":
		passed_college_id = request.GET['passed_college_id']

		if not passed_college_id:
			if acc_type == "Admin":
				return render(request, 'admin_misconducts.html', context)
			elif acc_type == "Chair":
				return render(request, 'chair_misconducts.html', context)

		else:
			queryset = College.objects.filter(college_id = passed_college_id)
			context = {
				"queryset": queryset
			}

			# add to audit trail
			action = ' edited college ' + queryset[0].name
			add_to_trail(action)

			if acc_type == "Admin":
				return render(request, 'admin_edit_college.html', context)
			elif acc_type == "Chair":
				return render(request, 'chair_edit_college.html', context)
	return HttpResponseRedirect("/login")

def edit_college_success(request):
	if login == 1:
		if request.method == "POST":
			passed_college_id = request.POST['college_id']
			passed_name = request.POST['name']
			
			College.objects.filter(college_id=passed_college_id).update(
							name = passed_name,
							)

			get_college = College.objects.filter(college_id=passed_college_id)

			# add to audit trail
			action = ' edited college ' + get_college[0].name
			add_to_trail(action)

			return HttpResponseRedirect("/colleges/")
	return HttpResponseRedirect("/login")

def delete_college(request):
	if login == 1:
		if request.method == "POST":
			passed_college_id = request.POST['college_id']
			delete_college = College.objects.filter(college_id = passed_college_id)

			# # add to audit trail
			action = ' deleted college ' + delete_college[0].name
			add_to_trail(action)

			# delete
			delete_college.delete()
		
		return HttpResponseRedirect("/colleges/")
	return HttpResponseRedirect("/login")

def add_college(request):
	if login == 1:
		if acc_type == "Admin":
			return render(request, 'admin_add_college.html') # use this instead!
			# return render_to_response('admin_add_college.html') comment out!!
		elif acc_type == "Chair":
			return render(request, 'chair_add_college.html')
			# return render_to_response('chair_add_college.html') comment out!! 
	return HttpResponseRedirect("/login")

def add_college_success(request):
	if login == 1:
		if request.method == "POST":

			# get id of last college in table
			queryset = College.objects.all()	# get list of colleges
			if len(queryset) != 0:
				last_id = queryset[len(queryset)-1].college_id  # get last id 
			else:
				last_id = 0

			passed_college_id = last_id + 1
			passed_name = request.POST['college_name']
			
			new_college = College(college_id=passed_college_id, name=passed_name)
	
			new_college.save()

			# add to audit trail
			action = ' added college ' + new_college.name
			add_to_trail(action)

		return HttpResponseRedirect("/colleges/")
	return HttpResponseRedirect("/login")

def departments(request):
	if login == 1:
		# code for showing all Departments
		queryset = Department.objects.all()
		
		context = {
			"queryset": queryset
		}

		# add to audit trail
		action = ' viewed all departments'
		add_to_trail(action)

		if acc_type == "Admin":
			return render(request, 'admin_departments.html', context)
		elif acc_type == "Chair":
			return render(request, 'chair_departments.html', context)
	return HttpResponseRedirect("/login")

def edit_department(request):
	if login == 1 and acc_type != "Member" and acc_type != "Staff":
		passed_department_id = request.GET['passed_department_id']	# passed_department_id is the value of misconduct_id from /cases

		if not passed_department_id:
			if acc_type == "Admin":
				return render(request, 'admin_departments.html', context)
			elif acc_type == "Chair":
				return render(request, 'chair_departments.html', context)

		else:
			queryset = Department.objects.filter(department_id = passed_department_id)	# get specific case using misconduct_id 
			colleges = College.objects.all()
			context = {
				"queryset": queryset,
				"colleges": colleges
			}

			# add to audit trail
			action = ' edited department ' + queryset[0].name
			add_to_trail(action)

			if acc_type == "Admin":
				return render(request, 'admin_edit_department.html', context)
			elif acc_type == "Chair":
				return render(request, 'chair_edit_department.html', context)
	return HttpResponseRedirect("/login")

def edit_department_success(request):
	if login == 1:
		if request.method == "POST":
			passed_department_id = request.POST['department_id']
			passed_college_name = request.POST['college_name']
			passed_name = request.POST['name']

			# get instance from College table
			get_college = College.objects.filter(name = passed_college_name)

			Department.objects.filter(department_id=passed_department_id).update(
							name = passed_name,
							college_id = get_college[0]
							)

			get_department = Department.objects.filter(department_id=passed_department_id)

			# add to audit trail
			action = ' edited college ' + get_department[0].name
			add_to_trail(action)

		return HttpResponseRedirect("/departments/")
	return HttpResponseRedirect("/login")

def delete_department(request):
	if login == 1:
		if request.method == "POST":
			passed_department_id = request.POST['department_id']
			delete_department = Department.objects.filter(department_id = passed_department_id)

			# # add to audit trail
			action = ' deleted department ' + delete_department[0].name
			add_to_trail(action)

			# delete
			delete_department.delete()
		
		return HttpResponseRedirect("/departments/")
	return HttpResponseRedirect("/login")

def add_department(request):
	if login == 1:

		# pass Colleges for dropdown option 
		queryset = College.objects.all()
		context = {
			"queryset": queryset
		}

		if acc_type == "Admin":
			return render(request, 'admin_add_department.html', context)
			# return render_to_response('admin_add_department.html')
		elif acc_type == "Chair":
			return render(request, 'chair_add_department.html', context)
			# return render_to_response('chair_add_department.html')
	return HttpResponseRedirect("/login")

def add_department_success(request):
	if login == 1:
		if request.method == "POST":
			# get id of last department in table
			queryset = Department.objects.all()	# get list of departments
			if len(queryset) != 0:
				last_id = queryset[len(queryset)-1].department_id  # get last id 
			else:
				last_id = 0

			passed_department_id = last_id + 1
			passed_name = request.POST['name']
			passed_college_name = request.POST['college_name'] # get the instance where instance.college_id = passed_college_id and yun ipasa mo
			
			# get instance from College table
			get_college = College.objects.filter(name = passed_college_name)

			new_department = Department(department_id=passed_department_id, name=passed_name, college_id=get_college[0])
	
			new_department.save()

			# add to audit trail
			action = ' added department ' + new_department.name
			add_to_trail(action)

		return HttpResponseRedirect("/departments/")
	return HttpResponseRedirect("/login")

def respondents(request):
	if login == 1:
		# code for showing all respondents
		queryset = Respondent.objects.all()
		
		context = {
			"queryset": queryset
		}

		# add to audit trail
		action = ' viewed all respondents'
		add_to_trail(action)

		if acc_type == "Staff":
			return render(request, 'staff_respondents.html', context)
	return HttpResponseRedirect("/login")

def edit_respondent(request):
	if login == 1 and acc_type == "Staff":
		passed_respondent_id = request.GET['passed_respondent_id']	

		if not passed_respondent_id:
			if acc_type == "Staff":
				return render(request, 'staff_respondent.html', context)

		else:
			queryset = Respondent.objects.filter(respondent_id = passed_respondent_id)
			departments = Department.objects.all()
			context = {
				"queryset": queryset,
				"departments": departments
			}

			# add to audit trail
			action = ' edited respondents ' + queryset[0].last_name
			add_to_trail(action)

			if acc_type == "Staff":
				return render(request, 'staff_edit_respondent.html', context)
	return HttpResponseRedirect("/login")

def edit_respondent_success(request):
	if login == 1:
		if request.method == "POST":
			passed_respondent_id= request.POST['respondent_id']
			passed_last_name = request.POST['last_name']
			passed_first_name = request.POST['first_name']
			passed_middle_name = request.POST['middle_name']
			passed_degree_program = request.POST['degree_program']
			passed_department_name = request.POST['department_name']
			passed_is_student = request.POST['is_student']
			if passed_is_student == "Yes":
				passed_is_student = True
			elif passed_is_student == "No":
				passed_is_student = False

			# get instance from Department table
			get_department = Department.objects.filter(name = passed_department_name)
			
			# update 
			Respondent.objects.filter(respondent_id=passed_respondent_id).update(
							last_name = passed_last_name,
							first_name = passed_first_name,
							middle_name = passed_middle_name,
							degree_program = passed_degree_program,
							department_id = get_department[0],
							is_student = passed_is_student
							)


			get_respondent = Respondent.objects.filter(respondent_id=passed_respondent_id)

			# add to audit trail
			action = ' edited respondent ' + get_respondent[0].first_name + ' ' + get_respondent[0].last_name
			add_to_trail(action)

			return HttpResponseRedirect("/respondents/")
	return HttpResponseRedirect("/login")

def delete_respondent(request):
	if login == 1:
		if request.method == "POST":
			passed_respondent_id = request.POST['respondent_id']
			delete_respondent = Respondent.objects.filter(respondent_id = passed_respondent_id)

			# # add to audit trail
			action = ' deleted respondent ' + delete_respondent[0].first_name + ' ' + delete_respondent[0].last_name 
			add_to_trail(action)

			# delete
			delete_respondent.delete()
		
		return HttpResponseRedirect("/respondents/")
	return HttpResponseRedirect("/login")

def add_respondent(request):
	if login == 1:

		# pass Departments for dropdown option 
		queryset = Department.objects.all()
		context = {
			"queryset": queryset
		}

		if acc_type == "Staff":
			return render(request, 'staff_add_respondent.html', context)
	return HttpResponseRedirect("/login")

def add_respondent_success(request):
	if login == 1:
		if request.method == "POST":
			# get input 
			passed_last_name = request.POST['last_name']
			passed_first_name = request.POST['first_name']
			passed_middle_name = request.POST['middle_name']
			passed_degree_program = request.POST['degree_program']
			passed_department_name = request.POST['department_name']
			passed_is_student = request.POST['is_student']
			if passed_is_student == "Yes":
				passed_is_student = True
			elif passed_is_student == "No":
				passed_is_student = False

			# get instance from Department table
			get_department = Department.objects.filter(name = passed_department_name)

			# get last id in table
			queryset = Respondent.objects.all()	# get list of departments
			if len(queryset) != 0:
				last_id = queryset[len(queryset)-1].respondent_id  # get last id 
			else:
				last_id = 0

			# insert to database
			new_respondent = Respondent(respondent_id = last_id + 1,
			    last_name = passed_last_name,
			    first_name = passed_first_name,
			    middle_name = passed_middle_name,
			    degree_program = passed_degree_program,
			    department_id = get_department[0],
			    is_student = passed_is_student)

			new_respondent.save()

			# add to audit trail
			action = ' added new respondent'
			add_to_trail(action)

		return HttpResponseRedirect("/respondents/")
	return HttpResponseRedirect("/login")

def univ_reps(request):
	if login == 1:
		# code for showing all univ reps
		queryset = univ_rep.objects.all()
		
		context = {
			"queryset": queryset
		}

		# add to audit trail
		action = ' viewed all univ reps'
		add_to_trail(action)

		if acc_type == "Staff":
			return render(request, 'staff_univ_reps.html', context)
	return HttpResponseRedirect("/login")

def edit_univ_rep(request):
	if login == 1 and acc_type == "Staff":
		passed_rep_id = request.GET['passed_rep_id']	# passed_rep_id is the value of misconduct_id from /cases

		if not passed_rep_id:
			if acc_type == "Staff":
				return render(request, 'staff_univ_reps.html', context)

		else:
			queryset = univ_rep.objects.filter(rep_id = passed_rep_id)	# get specific case using misconduct_id 
			departments = Department.objects.all()
			context = {
				"queryset": queryset,
				"departments": departments
			}

			# add to audit trail
			action = ' edited univ rep ' + queryset[0].last_name
			add_to_trail(action)

			if acc_type == "Staff":
				return render(request, 'staff_edit_univ_rep.html', context)
	return HttpResponseRedirect("/login")

def edit_univ_rep_success(request):
	if login == 1:
		if request.method == "POST":
			passed_rep_id = request.POST['rep_id']
			passed_last_name = request.POST['last_name']
			passed_first_name = request.POST['first_name']
			passed_department_name = request.POST['department_name']

			# get instance from Department table
			get_department = Department.objects.filter(name = passed_department_name)
			
			# update
			univ_rep.objects.filter(rep_id=passed_rep_id).update(
							last_name = passed_last_name,
							first_name = passed_first_name,
							department_id = get_department[0]
							)

			get_rep = univ_rep.objects.filter(rep_id=passed_rep_id)

			# add to audit trail
			action = ' edited rep ' + get_rep[0].first_name + ' ' + get_rep[0].last_name
			add_to_trail(action)

			return HttpResponseRedirect("/univ_reps/")
	return HttpResponseRedirect("/login")

def delete_univ_rep(request):
	if login == 1:
		if request.method == "POST":
			passed_rep_id = request.POST['rep_id']
			delete_rep = univ_rep.objects.filter(rep_id = passed_rep_id)

			# # add to audit trail
			action = ' deleted rep ' + delete_rep[0].first_name + ' ' + delete_rep[0].last_name
			add_to_trail(action)

			# delete
			delete_rep.delete()
		
		return HttpResponseRedirect("/univ_reps/")
	return HttpResponseRedirect("/login")

def add_univ_rep(request):
	if login == 1:

		# pass Departments for dropdown option 
		queryset = Department.objects.all()
		context = {
			"queryset": queryset
		}

		if acc_type == "Staff":
			return render(request, 'staff_add_univ_rep.html', context)
	return HttpResponseRedirect("/login")

def add_univ_rep_success(request):
	if login == 1:
		if request.method == "POST":
			# get input 
			passed_last_name = request.POST['last_name']
			passed_first_name = request.POST['first_name']
			passed_department_name = request.POST['department_name']

    		# get instance from Department table
			get_department = Department.objects.filter(name = passed_department_name)

    		# get last id in table
			queryset = univ_rep.objects.all()	# get list of departments
			if len(queryset) != 0:
				last_id = queryset[len(queryset)-1].rep_id  # get last id 
			else:
				last_id = 0

			# insert to database
			new_univ_rep = univ_rep(rep_id = last_id + 1,
			    last_name = passed_last_name,
			    first_name = passed_first_name,
			    department_id = get_department[0])

			new_univ_rep.save()

			# add to audit trail
			action = ' added new university representative'
			add_to_trail(action)

		return HttpResponseRedirect("/univ_reps/")
	return HttpResponseRedirect("/login")

def ahdhc_member(request):
	if login == 1:
		# code for showing all ahdhc members
		queryset = ahdhc_members.objects.all()
		
		context = {
			"queryset": queryset
		}

		# add to audit trail
		action = ' viewed all AHDHC members'
		# add_to_trail(action)

		if acc_type == "Chair":
			return render(request, 'chair_ahdhc_member.html', context)
	return HttpResponseRedirect("/login")

def edit_ahdhc_member(request):
	if login == 1 and acc_type == "Chair":
		passed_member_id = request.GET['passed_member_id']	# passed_rep_id is the value of misconduct_id from /cases

		if not passed_member_id:
			if acc_type == "Chair":
				return render(request, 'chair_ahdhc_member.html', context)

		else:
			queryset = ahdhc_members.objects.filter(member_id = passed_member_id)	# get specific case using misconduct_id 
			departments = Department.objects.all()
			context = {
				"queryset": queryset,
				"departments": departments
			}

			# add to audit trail
			action = ' edited AHDHC Member' + queryset[0].last_name
			# add_to_trail(action)

			if acc_type == "Chair":
				return render(request, 'chair_edit_ahdhc_member.html', context)
	return HttpResponseRedirect("/login")

def edit_ahdhc_member_success(request):
	if login == 1:
		if request.method == "POST":
			passed_member_id = request.POST['member_id']
			passed_last_name = request.POST['last_name']
			passed_first_name = request.POST['first_name']
			passed_department_name = request.POST['department_name']
			passed_is_student = request.POST['is_student']
			if passed_is_student == "Yes":
				passed_is_student = True
			elif passed_is_student == "No":
				passed_is_student = False

			# get instance from Department table
			get_department = Department.objects.filter(name = passed_department_name)
			
			# update
			ahdhc_members.objects.filter(member_id=passed_member_id).update(
							last_name = passed_last_name,
							first_name = passed_first_name,
							department_id = get_department[0],
							is_student = passed_is_student
							)

			get_mem = ahdhc_members.objects.filter(member_id=passed_member_id)

			# add to audit trail
			action = ' edited AHDHC Member ' + get_mem[0].last_name
			# add_to_trail(action)

			return HttpResponseRedirect("/ahdhc_member/")
	return HttpResponseRedirect("/login")

def delete_ahdhc_member(request):
	if login == 1:
		if request.method == "POST":
			passed_member_id = request.POST['member_id']
			delete_mem = ahdhc_members.objects.filter(member_id = passed_member_id)

			# # add to audit trail
			action = ' deleted AHDHC Member ' + delete_mem[0].last_name
			# add_to_trail(action)

			# delete
			delete_mem.delete()
		
		return HttpResponseRedirect("/univ_reps/")
	return HttpResponseRedirect("/login")

def add_ahdhc_member(request):
	if login == 1:

		queryset = Department.objects.all()
		context = {
			"queryset": queryset
		}

		if acc_type == "Chair":
			return render(request, 'chair_add_ahdhc_member.html', context)
	return HttpResponseRedirect("/login")

def add_ahdhc_member_success(request):
	if login == 1:
		if request.method == "POST":
			# get input 
			passed_last_name = request.POST['last_name']
			passed_first_name = request.POST['first_name']
			passed_department_name = request.POST['department_name']
			passed_is_student = request.POST['is_student']
			if passed_is_student == "Yes":
				passed_is_student = True
			elif passed_is_student == "No":
				passed_is_student = False

    		# get instance from Department table
			get_department = Department.objects.filter(name = passed_department_name)

    		# get last id in table
			queryset = ahdhc_members.objects.all()	# get list of departments
			if len(queryset) != 0:
				last_id = queryset[len(queryset)-1].member_id  # get last id 
			else:
				last_id = 0

			# insert to database
			new_member = ahdhc_members(member_id = last_id + 1,
			    last_name = passed_last_name,
			    first_name = passed_first_name,
			    department_id = get_department[0],
			    is_student = passed_is_student)

			new_member.save()

			# add to audit trail
			action = ' added new AHDHC member'
			# add_to_trail(action)

		return HttpResponseRedirect("/ahdhc_member/")
	return HttpResponseRedirect("/login")