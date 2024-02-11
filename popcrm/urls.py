from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views


from core.views import *
from userprofile.views import signup, myaccount

urlpatterns = [
    #Core
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('about/',about, name="about"),
    #path("stripe/", include("djstripe.urls", namespace="djstripe")),

    #userprofile
    path('', include('userprofile.urls')),

    #Dashboard
    path('dashboard/', include('dashboard.urls')),

    #Leads
    path('dashboard/leads/', include('lead.urls')),

    #clients
    path('dashboard/clients/', include('client.urls')),

    #teams
    path('dashboard/teams/', include('team.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
