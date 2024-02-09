from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_post')
    title = models.CharField(max_length=200, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)       # 수정 일시
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_post')

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)    # 수정 일시
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_comment')
