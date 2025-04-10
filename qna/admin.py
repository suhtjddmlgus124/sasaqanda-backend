from django.contrib import admin
from .models.question import Question, SubjectCategory, Tag, TagCategory


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(SubjectCategory, CategoryAdmin)


admin.site.register(TagCategory)


admin.site.register(Tag)