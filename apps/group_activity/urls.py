from django.urls import path
from .views import *

app_name = 'group_activity'

urlpatterns = [
    path('main/<int:room_id>', show_activity_main, name="main_page"),
    path('member_list/<int:room_id>', show_member_list, name="member_list"),
    path('permission_check', permission_check, name='permission_check'),
]