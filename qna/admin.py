from django.contrib import admin
from .models.subject import SubjectCategory
from .models.tag import TagCategory, Tag


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(SubjectCategory, CategoryAdmin)


admin.site.register(TagCategory)


admin.site.register(Tag)