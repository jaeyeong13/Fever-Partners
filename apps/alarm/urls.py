from django.urls import path
from . import views

app_name = 'alarm'

urlpatterns = [
    path('show_alarms', views.show_alarms, name='show_alarms'),
    path('alarm_detail/<int:pk>/', views.alarm_detail, name='alarm_detail'),
    path('accept_request/<int:alarm_id>/', views.accept_request, name='accept_request'),
    path('reject_request/<int:alarm_id>/', views.reject_request, name='reject_request'),
]