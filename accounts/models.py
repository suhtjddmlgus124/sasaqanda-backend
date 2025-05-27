from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('STUDENT', '학생'),
        ('TEACHER', '선생님'),
        ('STAFF', '관리자'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    token = models.IntegerField(default=100)
    mastery = models.IntegerField(default=0)

    def __str__(self):
        return f"[{self.get_role_display()}] {self.username}"