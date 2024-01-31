from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path("", views.start, name="start"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("signup/email/", views.user_signup_email, name="signup_email"),
    path("nickname/", views.user_nickname, name="nickname"),
    path("main/", views.main, name="main"),
    path("logout/", views.user_logout, name="logout"),
]