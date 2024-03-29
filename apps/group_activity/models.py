from django.db import models
from django.contrib.auth import get_user_model
from apps.group_management.models import Room
from django.utils import timezone
import datetime

User = get_user_model()

#그룹장이 만드는 인증
class Authentication(models.Model):
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    start = models.TimeField('인증시작', default=datetime.time(0, 0))
    end = models.TimeField('인증종료', default=datetime.time(2, 0))

#그룹에서 하는 인증
class MemberAuthentication(models.Model):
    room = models.ForeignKey(Room, related_name='auth_room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='auth_user', on_delete=models.CASCADE)
    is_auth = models.BooleanField(default=False)
    content = models.CharField('인증내용', max_length=100, null=True)
    image = models.ImageField('인증사진', upload_to='authentication_images/', null=True)
    is_completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
