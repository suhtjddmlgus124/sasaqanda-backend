from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(default=False)

    def __str__(self):
        return self.title