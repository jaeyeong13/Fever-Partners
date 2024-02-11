from django.urls import path
from .views import *

app_name = 'group_activity'

urlpatterns = [
    path('main/<int:room_id>', show_activity_main, name="main_page"),
    path('activate/<int:pk>/', activate, name='activate'),
    path('authentication/<int:pk>', create_authentication, name='create_authentication'),
    path('auth/<int:pk>', create_auth, name='create_auth'),
    path('verify/<int:pk>/', verify, name='verify'),
    path('accept_auth_log/<int:pk>', accept_auth_log, name='accept_auth_log'),
    path('refuse_auth_log/<int:pk>', refuse_auth_log, name='refuse_auth_log'),
    path('show_log/<int:pk>', show_log, name='show_log'),
    path('member_list/<int:room_id>', show_member_list, name="member_list"),
    path('permission_check', permission_check, name='permission_check'),
    path('withdraw_from_room', withdraw_from_room, name='withdraw_from_room'),
]