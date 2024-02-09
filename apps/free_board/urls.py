# from django.urls import path
# from . import views
# from .views import *
#
# app_name = 'free_board'
#
# urlpatterns = [
#   path('', board_list, name='list'),    # /board/ 접속 시 볼 수 있는 화면
#   path('<int:post_id>/', post_detail, name='detail'),
#   path('comments/create/<int:post_id>/', create_comment, name='create_comment'),
#   path('posts/create/', create_post, name='create_post'),
# ]

from django.urls import path
from . import views

app_name = 'free_board'

urlpatterns = [
  path('', views.index, name='list'),  # 메인 페이지로 `index` 뷰 함수 사용
  path('<int:post_id>/', views.post_detail, name='detail'),
  path('comments/create/<int:post_id>/', views.create_comment, name='create_comment'),
  path('posts/create/', views.create_post, name='create_post'),
  path('posts/modify/<int:post_id>/', views.modify_post, name='modify_post'),
  path('posts/delete/<int:post_id>/', views.post_delete, name='post_delete'),
  path('comments/modify/<int:comment_id>/', views.modify_comment, name='modify_comment'),
  path('comments/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]
