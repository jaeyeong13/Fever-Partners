from django.db import models
from django.contrib.auth import get_user_model

class Tag(models.Model):
    tag_name = models.CharField(max_length=10)
    parent_tag = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.tag_name

class ActivityTag(models.Model):
    tag_name = models.CharField(max_length=10)

    def __str__(self):
        return self.tag_name

class Goal(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, default=None)
    activityTags = models.ManyToManyField(ActivityTag, default=None)
    title = models.CharField(max_length=50)
    content = models.TextField()
    favor_offline = models.BooleanField(default=False)