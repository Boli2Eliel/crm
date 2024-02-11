
from django.urls import path
from lead import views

app_name = 'leads'

urlpatterns = [
    #Core
    path('leads-list/', views.LeadListAllView.as_view(), name='list_all'),
    path('', views.LeadListView.as_view(), name='list'),

    path('<int:pk>/', views.LeadDetailAllView.as_view(), name='detail_all'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='detail'),

    path('<int:pk>/delete', views.LeadDeleteForSuperUserView.as_view(), name='delete_spuser'),
    path('<int:pk>/delete', views.LeadDeleteView.as_view(), name='delete'),

    path('<int:pk>/edit/', views.LeadUpdateAllView.as_view(), name="edit_all"),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(), name="edit"),

    path('<int:pk>/add-comment/', views.AddCommentView.as_view(), name="add_comment"),
    path('<int:pk>/add-file/', views.AddFileView.as_view(), name="add_file"),
    path('add/', views.LeadCreateView.as_view(), name="add"),
    path('<int:pk>/convert/', views.ConvertToClientView.as_view(), name="convert"),

    #path('', views.leads_list, name='list'),
    #path('<int:pk>/', views.leads_detail, name="detail"),
    #path('add_lead/', views.leads_add, name="add"),
    #path('<int:pk>/edit/', views.leads_edit, name="edit"),
    #path('<int:pk>/delete', views.leads_delete, name="delete"),
    #path('<int:pk>/convert/', views.convert_to_client, name="convert"),

]
