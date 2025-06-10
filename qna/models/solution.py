from django.db import models
from django.utils import timezone
import os
import uuid
from .question import Question
from accounts.models import User

def teacher_solution_upload(instance, filename):
    ext = filename.split('.')[-1]
    today = timezone.now().strftime("%Y/%m/%d")
    name = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('solutions', 'teacher', today, name)

class TeacherSolution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='teacher_solutions')
    image = models.ImageField(upload_to=teacher_solution_upload)

    def __str__(self):
        return f"{self.question.id}번 문제 선생님의 풀이"


def student_solution_upload(instance, filename):
    ext = filename.split('.')[-1]
    today = timezone.now().strftime("%Y/%m/%d")
    name = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('solutions', 'student', today, name)

class StudentSolution(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='student_solutions')
    image = models.ImageField(upload_to=student_solution_upload)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='solutions')

    def __str__(self):
        return f"{self.question.id}번 문제 {self.author.username}의 풀이"


class LikeEnrollment(models.Model):
    question = models.ForeignKey(StudentSolution, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')