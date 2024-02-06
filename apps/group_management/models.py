from django.db import models
from django.contrib.auth import get_user_model
from apps.goal_management.models import Tag, ActivityTag

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