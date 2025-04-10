from django.db import models
from accounts.models import User


class SubjectCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT, related_name='subcategories')

    def get_breadcrumb(self):
        ret = [{'id': self.id, 'name': self.name}]
        parent = self.parent
        while parent:
            ret.insert(0, {'id':parent.id, 'name':parent.name})
            parent = parent.parent
        return ret
    
    def __str__(self):
        return f"{self.name} ({'>'.join([i['name'] for i in self.get_breadcrumb()])})"
        

class TagCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')

    def get_breadcrumb(self):
        ret = [{'id': self.id, 'name': self.name}]
        parent = self.parent
        while parent:
            ret.insert(0, {'id': parent.id, 'name': parent.name})
            parent = parent.parent
        return ret
    
    def __str__(self):
        return f"{self.name} ({'>'.join([i['name'] for i in self.get_breadcrumb()])})"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    tag_category = models.ForeignKey(TagCategory, on_delete=models.PROTECT, related_name='tags')

    def __str__(self):
        return f"{self.name} ({self.tag_category.name})"
    

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