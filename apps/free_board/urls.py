from django.urls import path
from .views import *

app_name = 'free_board'

urlpatterns = [
  path('free_board/', create_post, name='create_post')
]