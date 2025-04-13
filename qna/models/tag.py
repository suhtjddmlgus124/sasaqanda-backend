from django.db import models
from django.core.exceptions import ValidationError


class TagCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')

    def clean_parent(self):
        if self.parent == self:
            raise ValidationError("parent는 자신이 될 수 없습니다")

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