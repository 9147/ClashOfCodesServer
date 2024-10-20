from django.contrib import admin
from .models import Team, ProblemSubmission, UserToken, submissiontime, contact

# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'leader_contact', 'member1_name', 'member2_name', 'member3_name']
    sortable_by = ['name', 'leader', 'leader_contact', 'member1_name', 'member2_name', 'member3_name']
    search_fields = ['name', 'leader', 'leader_contact', 'member1_name', 'member2_name', 'member3_name']
    list_filter = ['name', 'leader', 'leader_contact', 'member1_name', 'member2_name', 'member3_name']

@admin.register(ProblemSubmission)
class ProblemSubmissionAdmin(admin.ModelAdmin):
    list_display = ['team', 'problem_solution_file', 'submission_time', 'title', 'description', 'status']
    sortable_by = ['team', 'problem_solution_file', 'submission_time', 'title', 'description', 'status']
    search_fields = ['team', 'problem_solution_file', 'submission_time', 'title', 'description', 'status']
    list_filter = ['team', 'problem_solution_file', 'submission_time', 'title', 'description', 'status']

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'token_created_at']
    sortable_by = ['user', 'token', 'token_created_at']
    search_fields = ['user', 'token', 'token_created_at']
    list_filter = ['user', 'token', 'token_created_at']

@admin.register(submissiontime)
class submissiontimeAdmin(admin.ModelAdmin):
    list_display = ['tag', 'submission_time']
    sortable_by = ['tag', 'submission_time']
    search_fields = ['tag', 'submission_time']
    list_filter = ['tag', 'submission_time']


@admin.register(contact)
class contactAdmin(admin.ModelAdmin):
    list_display = ['email', 'message','action']
    sortable_by = ['email', 'message','action']
    search_fields = ['email', 'message','action']
    list_filter = ['email', 'message','action']
