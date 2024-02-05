from django.urls import path
from . import views
from .views import *

app_name = 'free_board'

urlpatterns = [
  path('', create_post, name='list'),    # /board/ 접속 시 볼 수 있는 화면
  path('<int:post_id>/', post_detail, name='detail'),
  path('comments/create/<int:post_id>/', create_comment, name='create_comment'),
]
