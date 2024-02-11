from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from lead.models import Lead, Comment, LeadFile

# Register your models here.
class LeadAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'status', 'priority', 'created_by')

class CommentAdmin(ImportExportModelAdmin):
    list_display = ('created_by', 'content', 'created_at')

class LeadFileAdmin(ImportExportModelAdmin):
    list_display = ('created_by', 'file', 'created_at')

admin.site.register(Lead, LeadAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(LeadFile, LeadFileAdmin)