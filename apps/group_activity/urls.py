from django.urls import path
from .views import *

app_name = 'group_activity'

urlpatterns = [
    path('main/<int:room_id>', show_activity_main, name="main_page"),
]