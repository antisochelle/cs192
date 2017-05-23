from django.contrib import admin
from myapp.models import Users
from myapp.models import UsersRole
from myapp.models import Cases
from myapp.models import College
from myapp.models import Department
from myapp.models import Misconduct
from myapp.models import Respondent
from myapp.models import univ_rep

from myapp.models import ahdhc_members
from myapp.models import audit_trail
from myapp.models import cases_ahdhc_members
from myapp.models import cases_hearings
from myapp.models import cases_misconducts_respondents
from myapp.models import Announcements

# Register your models here.
admin.site.register(Users)
admin.site.register(UsersRole)
admin.site.register(Cases)
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Misconduct)
admin.site.register(Respondent)
admin.site.register(univ_rep)

admin.site.register(ahdhc_members)
admin.site.register(audit_trail)
admin.site.register(cases_ahdhc_members)
admin.site.register(cases_hearings)
admin.site.register(cases_misconducts_respondents)
admin.site.register(Announcements)