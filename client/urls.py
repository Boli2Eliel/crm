
from django.urls import path
from client import views

app_name = 'clients'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='list'),
    path('clients-list/', views.ClientListAllView.as_view(), name='list_all'),
    path('add-client/', views.ClientCreateView.as_view(), name="add"),
    path('<int:pk>/detail', views.ClientDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ClientUpdateView.as_view(), name="edit"),
    path('<int:pk>/add-comment/', views.clients_detail, name="add_comment"),
    path('<int:pk>/add-file/', views.clients_add_file, name="add_file"),
    path('<int:pk>/delete', views.ClientDeleteView.as_view(), name="delete"),
    path('export-csv/', views.clients_csv_export, name='export_csv'),
    #path('export-xls/', views.export_excel, name='export_xls'),

]
