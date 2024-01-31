from django.db import models
from apps.user_management.models import *

class Room(models.Model):
    name = models.CharField(max_length=100)
    master = models.ForeignKey(User, related_name='rooms_managed', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='rooms_joined')
    tags = models.CharField(max_length=100)
    rule = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AuthenticationImage(models.Model):
    room = models.ForeignKey(Room, related_name='authentication_images', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='authentication_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='authentication_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_authenticated = models.BooleanField('인증여부', default=False) #인증여부
