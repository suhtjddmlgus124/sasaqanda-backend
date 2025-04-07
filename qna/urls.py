from django.urls import path
from .views import categoryview


app_name = 'qna'

urlpatterns = [
    path('category/<int:category_id>/', categoryview.CategoryCreateRetrieveUpdateDestroyView.as_view(), name='category-create-retrieve-update-destroy'),
]