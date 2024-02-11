

from django.urls import path
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    #Core
    path('', views.dashboard, name="index"),

]
