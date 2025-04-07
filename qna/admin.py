from django.contrib import admin
from .models.question import Question, Category


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Category, CategoryAdmin)