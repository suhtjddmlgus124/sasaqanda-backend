from django.urls import path
from .views import announcementview


app_name = 'bulletinboard'

urlpatterns = [
    path('announcement/', announcementview.AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    path('announcement/<int:announcement_id>/', announcementview.AnnouncementRetrieveView.as_view(), name='announcement-retrieve'),
]