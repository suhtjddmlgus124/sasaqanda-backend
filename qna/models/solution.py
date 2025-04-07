from django.db import models
from .question import Question
from accounts.models import User


class TeacherSolution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='teacher_solutions')
    image = models.ImageField()


class StudentSolution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='student_solutions')
    image = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='solutions')


class LikeEnrollment(models.Model):
    question = models.ForeignKey(StudentSolution, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')