from django.db import models
from apps.user_management.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    master = models.ForeignKey(User, related_name='rooms_managed', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='rooms_joined')
    tags = models.CharField(max_length=100)
    rule = models.CharField(max_length=100)

    def __str__(self):
        return self.name
