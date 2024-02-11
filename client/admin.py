from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Client, Comment
# Register your models here.

class ClientAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'modified_at')

class CommentAdmin(ImportExportModelAdmin):
    list_display = ('created_by', 'content', 'created_at')

admin.site.register(Client, ClientAdmin)
admin.site.register(Comment, CommentAdmin)