from django.urls import path
from .views import *

app_name = 'user_management'

urlpatterns = [
    path('detail/<int:pk>', detail, name='detail'),
]