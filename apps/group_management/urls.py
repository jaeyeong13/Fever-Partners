from django.urls import path
from .views import *

app_name = 'group_management'

urlpatterns = [
    path('create_group/', start_creation, name='start_creation'),
    path('create_group/on_submit/', create_room, name='create_room'),
    path('member_recommendation/', show_user_list, name='recommendation_page'),
    path('group_list/', show_group_list, name='group_list')
]