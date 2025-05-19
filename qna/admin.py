from django.contrib import admin
from .models.subject import SubjectCategory
from .models.tag import TagCategory, Tag
from .models.question import Question
from .models.solution import StudentSolution, TeacherSolution


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(SubjectCategory, CategoryAdmin)


admin.site.register(TagCategory)


admin.site.register(Tag)


admin.site.register(Question)


admin.site.register(StudentSolution)
admin.site.register(TeacherSolution)