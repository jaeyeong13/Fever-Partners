from django.urls import path
from .views import *

app_name = 'goal_management'

urlpatterns = [
    path('create_goal/', start_creation, name='start_goal_creation'),
    path('get_subtags/<int:id>', get_subtags, name='get_subtag'),
    path('create_goal/on_submit', create_goal, name='create_goal'),
    path('ask_preference/', show_branching_point, name='show_branching_point'),
    path('goal_list/', goal_list, name="goal_list"),
    path('goal_update/', goal_update, name="goal_update"),
    path('group_recommendation/<int:goal_id>', recommend_group, name='recommendation_page'),
    path('delete_goal/<int:goal_id>', delete_goal, name='delete_goal'),
    path('suggest_join/<int:goal_id>', suggest_join, name='suggest_join'),
    path('achievement_report/<int:goal_id>', create_achievement_report, name='achievement_report'),
]