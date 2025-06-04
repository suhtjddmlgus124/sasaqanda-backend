from django.urls import path
from .views import authview, infoview, scoreboardview


app_name = 'account'

urlpatterns = [
    path('authentication/', authview.GoogleAuthenticationView.as_view(), name='authentication'),
    path('me/', infoview.UserIdentityView.as_view(), name='identity'),
    # path('authentication/', authview.AuthenticationView.as_view(), name='authentication'),
    # path('register/', authview.RegisterView.as_view(), name='register'),
    path('scoreboard/', scoreboardview.ScoreboardView.as_view(), name='scoreboard'),
]