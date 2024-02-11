from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db import models
from apps.group_management.models import Room  # Room 모델을 임포트


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_post')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_posts', null=True)  # Room 모델을 참조하는 필드 추가
    title = models.CharField(max_length=200, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_post')
    notice = models.BooleanField(default=False)  # 공지글 여부 체크하기

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)    # 수정 일시
    voter = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='voter_comment')

    def __str__(self):
        return self.content
