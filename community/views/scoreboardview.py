from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from accounts.serializers import UserPublicSerializer


class ScoreboardView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        users = User.objects.filter(role='STUDENT', is_active=True).order_by('-mastery')
        serializer = UserPublicSerializer(users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)