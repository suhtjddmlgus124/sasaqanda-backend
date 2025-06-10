from django.db import models
from django.utils import timezone
import os
import uuid
from .subject import SubjectCategory
from .tag import Tag
from accounts.models import User
from ..api import ocr
from ..api import gpt


def question_upload(instance, filename):
    ext = filename.split('.')[-1]
    today = timezone.now().strftime("%Y/%m/%d")
    name = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('questions', today, name)

class Question(models.Model):
    subject_category = models.ForeignKey(SubjectCategory, on_delete=models.PROTECT, null=True, related_name='questions')
    image = models.ImageField(upload_to=question_upload)
    content = models.TextField(blank=True)
    vector = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='questions')

    def get_content(self):
        data = ocr.call_ocr_api(self.image.open("rb"))
        if data["status"] == 200:
            self.content = data["text"]

    def get_vector(self):
        vector = gpt.call_gpt_api(self.content)
        self.vector = vector


# class TagEnrollment(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='tags')
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='questions')


class StarEnrollment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='stars')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stars')