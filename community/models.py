from django.db import models
from accounts.models import User


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Topic(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='topics')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)