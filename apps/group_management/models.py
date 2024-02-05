from django.db import models
from django.contrib.auth import get_user_model
from apps.goal_management.models import Tag, ActivityTag
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Room(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    members = models.ManyToManyField(User, related_name='members', default=None)
    master = models.ForeignKey(User, related_name='master', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, default=None)
    activityTags = models.ManyToManyField(ActivityTag, default=None)
    cert_required = models.BooleanField(default=False)
    cert_detail = models.TextField(null=True)
    penalty_value = models.PositiveIntegerField(default=0)
    favor_offline = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

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