from django.db import models
from django.contrib.auth import get_user_model
from apps.group_management.models import Room
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

#그룹장이 만드는 인증
class Authentication(models.Model):
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    start = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(24)])
    end = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(24)])

#그룹에서 하는 인증
class MemberAuthentication(models.Model):
    room = models.ForeignKey(Room, related_name='auth_room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='auth_user', on_delete=models.CASCADE)
    is_auth = models.BooleanField(default=False)
    content = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='authentication_images/', null=True)

#인증 로그
class AuthenticationLog(models.Model):
    room = models.ForeignKey(Room, related_name='log_auth_room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='log_auth_user', on_delete=models.CASCADE)
    authentication = models.ForeignKey(Authentication, related_name='log_auth', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_created=True, auto_now_add=True)