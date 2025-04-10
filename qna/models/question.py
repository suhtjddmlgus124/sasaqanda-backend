from django.db import models
from .subject import SubjectCategory
from .tag import Tag
from accounts.models import User


class Question(models.Model):
    subject_category = models.ForeignKey(SubjectCategory, on_delete=models.PROTECT, related_name='questions')

    image = models.ImageField()
    content = models.TextField()
    vector = models.JSONField()


class TagEnrollment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='questions')


class StarEnrollment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='stars')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stars')