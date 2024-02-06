from django.urls import path
from .views import *

app_name = 'group_activity'

urlpatterns = [
    path('main/<int:room_id>', show_activity_main, name="main_page"),
    path('activate/<int:pk>/', activate, name='activate'),
    path('authentication/<int:pk>', create_authentication, name='create_authentication'),
    path('auth/<int:pk>', create_auth, name='create_auth'),
    path('verify/<int:pk>/', verify, name='verify'),
]