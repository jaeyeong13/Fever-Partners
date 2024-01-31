from django.urls import path
from . import views

app_name = 'alarm'

urlpatterns = [
    path('delete/<int:pk>/', views.delete, name='delete'),
]