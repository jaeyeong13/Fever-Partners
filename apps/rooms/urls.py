from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'rooms'

urlpatterns = [
    path("", views.detail, name="detail"),
    path('upload_image/', views.upload_image, name='upload_image'),
]
