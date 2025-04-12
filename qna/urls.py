from django.urls import path
from .views import subjectview, tagview


app_name = 'qna'

urlpatterns = [
    path('subjectcategory/<int:subject_category_id>/', subjectview.SubjectCategoryCreateRetrieveUpdateDestroyView.as_view(), name='subject-category-create-retrieve-update-destroy'),
    
    path('tagcategory/', tagview.TagCategoryListView.as_view(), name='tag-category-list'),
    path('tagcategory/<int:tag_category_id>/', tagview.TagCategoryCreateRetrieveUpdateDestroyView.as_view(), name='tag-category-create-retrieve-update-destroy'),
    path('tagcategory/<int:tag_category_id>/createtag/', tagview.TagCreateView.as_view(), name='tag-create'),

    path('tag/<int:tag_id>/', tagview.TagRetrieveUpdateDeleteView.as_view(), name='tag-retrieve-update-delete'),
]