from django.contrib import admin
from .models.subject import SubjectCategory
from .models.tag import TagCategory, Tag
from .models.question import Question


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(SubjectCategory, CategoryAdmin)


admin.site.register(TagCategory)


admin.site.register(Tag)


admin.site.register(Question)