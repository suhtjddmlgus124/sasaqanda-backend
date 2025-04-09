from django.contrib import admin
from .models.question import Question, Category, Tag, TagCategory


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)


admin.site.register(TagCategory)


admin.site.register(Tag)