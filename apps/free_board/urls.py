from django.urls import path
from . import views
from .views import *

app_name = 'free_board'

urlpatterns = [
  path('', create_post, name='create_post'),    # /board/ 접속 시 볼 수 있는 화면
]
