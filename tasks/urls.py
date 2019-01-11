from django.urls import path, include
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:event_id>/', views.event, name='event'),
    path('<int:event_id>/register/', views.register, name='register'),
    path('<int:event_id>/register/<uuid:modifycode>/', views.modify_registration, name='modify_registration'),
    path('<int:event_id>/addperson/', views.addperson, name='addperson'),
    path('<int:event_id>/tasklist/', views.tasklist, name='tasklist'),
    path('<int:event_id>/create_tasks/', views.create_tasks, name='create_tasks'),
    path('<int:event_id>/message_all/', views.message_all, name='message_all'),
    path('i18n/', include('django.conf.urls.i18n')),
]
