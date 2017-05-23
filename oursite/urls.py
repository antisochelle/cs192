"""oursite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp import views as v
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', v.login_view), 
    url(r'^login/',  v.login_view),
    url(r'^logout/$', v.logout),
    url(r'^home/$', v.home),
    url(r'^cases/$', v.cases),
    url(r'^delete_case/$', v.delete_case),
    url(r'^add_announcement/$', v.add_announcement),
    url(r'^announcement_success/$', v.announcement_success),
    url(r'^view_case/$', v.view_case),
    url(r'^edit_case/$', v.edit_case),
    url(r'^edit_case_success/$', v.edit_case_success),
    url(r'^add_case/$', v.add_case),
    url(r'^case_success/$', v.case_success),
    url(r'^user_success/$', v.user_success),
    url(r'^users/$', v.users),
    url(r'^add_user/$', v.add_user),
    url(r'^delete_user/$', v.delete_user),
    url(r'^view_user/$', v.view_user),
    url(r'^edit_user_success/$', v.edit_user_success),
    url(r'^edit_user/$', v.edit_user),
    url(r'^misconducts/$', v.misconducts),
    url(r'^view_misconduct/$', v.view_misconduct),
    url(r'^view_trail/$', v.view_trail),
    url(r'^colleges/$', v.colleges),
    url(r'^departments/$', v.departments),
    url(r'^edit_misconduct/$', v.edit_misconduct),
    url(r'^edit_misconduct_success/$', v.edit_misconduct_success),
    url(r'^delete_misconduct/$', v.delete_misconduct),
    url(r'^edit_college/$', v.edit_college),
    url(r'^edit_college_success/$', v.edit_college_success),
    url(r'^delete_college/$', v.delete_college),
    url(r'^edit_department/$', v.edit_department),
    url(r'^edit_department_success/$', v.edit_department_success),
    url(r'^delete_department/$', v.delete_department),
    url(r'^add_college/$', v.add_college),
    url(r'^add_college_success/$', v.add_college_success),
    url(r'^add_misconduct/$', v.add_misconduct),
    url(r'^add_misconduct_success/$', v.add_misconduct_success),
    url(r'^add_department/$', v.add_department),
    url(r'^add_department_success/$', v.add_department_success),
    url(r'^univ_reps/$', v.univ_reps),
    url(r'^edit_univ_rep/$', v.edit_univ_rep),
    url(r'^edit_univ_rep_success/$', v.edit_univ_rep_success),
    url(r'^delete_univ_rep/$', v.delete_univ_rep),
    url(r'^add_univ_rep/$', v.add_univ_rep),
    url(r'^add_univ_rep_success/$', v.add_univ_rep_success),
    url(r'^respondents/$', v.respondents),
    url(r'^edit_respondent/$', v.edit_respondent),
    url(r'^edit_respondent_success/$', v.edit_respondent_success),
    url(r'^delete_respondent/$', v.delete_respondent),
    url(r'^add_respondent/$', v.add_respondent),
    url(r'^add_respondent_success/$', v.add_respondent_success),
    url(r'^ahdhc_member/$', v.ahdhc_member),
    url(r'^edit_ahdhc_member/$', v.edit_ahdhc_member),
    url(r'^edit_ahdhc_member_success/$', v.edit_ahdhc_member_success),
    url(r'^delete_ahdhc_member/$', v.delete_ahdhc_member),
    url(r'^add_ahdhc_member/$', v.add_ahdhc_member),
    url(r'^add_ahdhc_member_success/$', v.add_ahdhc_member_success),
]

urlpatterns += staticfiles_urlpatterns()