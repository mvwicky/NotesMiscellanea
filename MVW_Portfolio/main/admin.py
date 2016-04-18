from django.contrib import admin

# Register your models here.
from .models import Job, VolunteerPos, Activity, Award

class JobAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['company_name', 'job_title']}),
		('Date Information', {'fields': ['start_date', 'end_date']})
		]

class VolunteerPosAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['site', 'organization', 'title']}),
		('Date Information', {'fields': ['start_date', 'end_date', 'num_hours']})
		]

admin.site.register(Job, JobAdmin)
admin.site.register(VolunteerPos, VolunteerPosAdmin)
admin.site.register(Activity)
admin.site.register(Award)