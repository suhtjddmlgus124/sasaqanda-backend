from django.db import models


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