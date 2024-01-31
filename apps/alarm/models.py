from django.db import models
from apps.rooms.models import Room
from apps.user_management.models import User

class Alarm(models.Model):
    alarm_from = models.ForeignKey(Room, related_name='sent_alarms', on_delete=models.CASCADE)
    alarm_to = models.ForeignKey(User, related_name='received_alarms', on_delete=models.CASCADE)
