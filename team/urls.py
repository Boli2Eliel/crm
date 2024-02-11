
from django.urls import path
from team import views

app_name = 'team'

urlpatterns = [
    #Core
    path('', views.teams_list, name='list'),
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/edit/', views.team_edit, name="edit"),
    path('<int:pk>/activate/', views.teams_activate, name="activate"),



]
