from django.urls import path
from .views import announcementview, scoreboardview


app_name = 'community'

urlpatterns = [
    path('announcement/', announcementview.AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    path('announcement/<int:announcement_id>/', announcementview.AnnouncementRetrieveView.as_view(), name='announcement-retrieve'),
    path('scoreboard/', scoreboardview.ScoreboardView.as_view(), name='scoreboard'),
]