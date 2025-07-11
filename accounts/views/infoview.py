from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers import UserIdentitySerializer
from qna.serializers.solution import StudentSolutionSerializer


class UserIdentityView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        user = request.user
        serializer = UserIdentitySerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
    

class MySolutionView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        user = request.user
        solutions = user.solutions
        serializer = StudentSolutionSerializer(solutions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)