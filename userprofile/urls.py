
from django.urls import path
from django.contrib.auth import views
from .views import myaccount, signup
from .forms import LoginForm

app_name = 'userprofile'

urlpatterns = [

    path('dashboard/myaccount/', myaccount, name="myaccount"),

    path('signup/', signup, name="signup"),
    path('log-in/', views.LoginView.as_view(template_name="userprofile/login.html", authentication_form=LoginForm), name="login"),
    path('log-out/', views.LogoutView.as_view(), name="logout"),



]
