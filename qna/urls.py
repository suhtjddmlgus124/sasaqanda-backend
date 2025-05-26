from django.urls import path
from .views import subjectview, tagview, questionview, solutionview
from django.conf import settings
from django.conf.urls.static import static


app_name = 'qna'

urlpatterns = [
    path('subjectcategory/<int:subject_category_id>/', subjectview.SubjectCategoryCreateRetrieveUpdateDestroyView.as_view(), name='subject-category-create-retrieve-update-destroy'),
    
    path('tagcategory/', tagview.TagCategoryListView.as_view(), name='tag-category-list'),
    path('tagcategory/<int:tag_category_id>/', tagview.TagCategoryCreateRetrieveUpdateDestroyView.as_view(), name='tag-category-create-retrieve-update-destroy'),
    path('tagcategory/<int:tag_category_id>/createtag/', tagview.TagCreateView.as_view(), name='tag-create'),

    path('tag/<int:tag_id>/', tagview.TagRetrieveUpdateDeleteView.as_view(), name='tag-retrieve-update-delete'),

    path('question/', questionview.QuestionCreateView.as_view(), name='question-create'),
    path('question/<int:question_id>/', questionview.QuestionRetrieveDeleteView.as_view(), name='question-retrieve-delete'),
    path('question/search/', questionview.QuestionSearchView.as_view(), name='question-search'),
    path('question/imageconvert/', questionview.QuestionImageConvertView.as_view(), name='question-image-convert'),

    path('question/<int:question_id>/teachersolution/', solutionview.TeacherSolutionListCreateView.as_view(), name='teacher-solution-list-create'),
    path('teachersolution/<int:solution_id>/', solutionview.TeacherSolutionRetrieveView.as_view(), name='teacher-solution-retrieve'),
    path('question/<int:question_id>/studentsolution/', solutionview.StudentSolutionListCreateView.as_view(), name='student-solution-list-create'),
    path('studentsolution/<int:solution_id>/', solutionview.StudentSolutionRetrieveView.as_view(), name='student-solution-retrieve'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document=settings.MEDIA_ROOT)