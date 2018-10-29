from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:event_id>/', views.event, name='event'),
    path('<int:event_id>/register', views.register, name='register'),
    path('<int:event_id>/addperson/', views.addperson, name='addperson'),
    path('<int:event_id>/tasklist/', views.tasklist, name='tasklist'),
]
