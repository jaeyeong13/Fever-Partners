from django.urls import path
from . import views

app_name = 'alarm'

urlpatterns = [
    path('alarm_list', views.alarm_list, name='alarm_list'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]