from django.urls import path
from .views import announcementview, scoreboardview, topicview


app_name = 'community'

urlpatterns = [
    path('announcement/', announcementview.AnnouncementListCreateView.as_view(), name='announcement-list-create'),
    path('announcement/<int:announcement_id>/', announcementview.AnnouncementRetrieveView.as_view(), name='announcement-retrieve'),
    
    path('scoreboard/', scoreboardview.ScoreboardView.as_view(), name='scoreboard'),

    path('topic/', topicview.TopicListCreateView.as_view(), name='topic-list-create'),
    path('topic/<int:topic_id>/', topicview.TopicRetrieveUpdateDestroyView.as_view(), name='topic-retrieve-update-destroy'),
]