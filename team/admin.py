from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from team.models import Team, Plan

# Register your models here.

class TeamAdmin(ImportExportModelAdmin):
    list_display = ('name', )

class PlanAdmin(ImportExportModelAdmin):
    list_display = ('name', 'price', 'description')


admin.site.register(Team, TeamAdmin)
admin.site.register(Plan, PlanAdmin)