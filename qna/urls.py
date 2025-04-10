from django.urls import path
from .views import categoryview


app_name = 'qna'

urlpatterns = [
    path('subjectcategory/<int:subject_category_id>/', categoryview.SubjectCategoryCreateRetrieveUpdateDestroyView.as_view(), name='subject-category-create-retrieve-update-destroy'),
    path('tagcategory/<int:tag_category_id>/', categoryview.TagCategoryCreateRetrieveUpdateDestroyView.as_view(), name='tag-category-create-retrieve-update-destroy'),
]