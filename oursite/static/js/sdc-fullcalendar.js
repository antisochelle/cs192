{% extends "admin_dashboard.html" %}
$(document).ready(function() {

// gets the current date
var date = new Date();
var d = date.getDate();
var m = date.getMonth();
var y = date.getFullYear();

$('#calendar').fullCalendar({

<!--Header Section Including Previous Next and Today-->
header: {
left: 'prev,next today',
center: 'title',
right: 'month,basicWeek,basicDay'
},

// view full event details on click
eventClick: function(calEvent, jsEvent, view) {
    alert('Reminder: ' + calEvent.title);
}, 

<!--Default Date-->
defaultDate: date,
editable: true,

<!--Event Section-->
eventLimit: true, // allow "more" link when too many events
events: [
    {% for case in cmr %}
        // displays Respondent Name
        {% if case.case_id.complaint_sdc_receipt_deadline %}
            {
                title: "SDC Complaint Receipt Deadline: Respondent " 
                    + "{{ case.respondent_id.first_name }}" 
                    + " {{ case.respondent_id.last_name }}",
                
                start: "{{ case.case_id.complaint_sdc_receipt_deadline|date:"Y-m-d" }}"
            },
        {% endif %} 
        {% if case.case_id.initial_report_deadline %}
            {
                title: "Initial Report Deadline: Respondent " 
                    + "{{ case.respondent_id.first_name }}" 
                    + " {{ case.respondent_id.last_name }}",
                
                start: "{{ case.case_id.initial_report_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.adr_deadline %}
            {
                title: "ADR Deadline: Respondent " 
                    + "{{ case.respondent_id.first_name }}" 
                    + " {{ case.respondent_id.last_name }}",
                
                start: "{{ case.case_id.adr_deadline|date:"Y-m-d" }}"
            },
        {% endif %}

        // displays Case Number
        {% if case.case_id.ahdhc_constitution_deadline %}
            {
                title: "AHDHC Constitution Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.ahdhc_constitution_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.summons_issuance_deadline %}
            {
                title: "Summons Issuance Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.summons_issuance_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.summons_service_deadline %}
            {
                title: "Summons Service Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.summons_service_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.summons_receipt_deadline %}
            {
                title: "Summons Receipt Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.summons_receipt_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.respondent_answer_deadline %}
            {
                title: "Respondent Answer Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.respondent_answer_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.preliminary_meeting_notice_deadline %}
            {
                title: "Preliminary Meeting Notice Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.preliminary_meeting_notice_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.case_resolution_deadline %}
            {
                title: "Case Resolution Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.case_resolution_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.final_committee_report_deadline %}
            {
                title: "Final Committee Report Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.final_committee_report_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.decision_issuance_deadline %}
            {
                title: "Decision Issuance Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.decision_issuance_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.decision_copy_to_chancellor_deadline %}
            {
                title: "Decision Copy to Chancellor Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.decision_copy_to_chancellor_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
        {% if case.case_id.appeal_deadline %}
            {
                title: "Appeal Deadline: Case No. "
                    + "{{ case.case_id.case_number }}",
                
                start: "{{ case.case_id.appeal_deadline|date:"Y-m-d" }}"
            },
        {% endif %}
    {% endfor %}
]
});
});