from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Userprofile

# Register your models here.

class UserprofileAdmin(ImportExportModelAdmin):
    list_display = ['user',]

admin.site.register(Userprofile, UserprofileAdmin)