from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from ..models.question import Question
from ..models.solution import TeacherSolution, StudentSolution
from ..serializers.solution import TeacherSolutionSerializer, StudentSolutionSerializer

from utils.response import NOT_FOUND_RESPONSE


class TeacherSolutionRetrieveView(APIView):
    permission_classes = [ AllowAny ]

    def get(self, request, solution_id):
        try:
            solution = TeacherSolution.objects.get(id=solution_id)
        except TeacherSolution.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = TeacherSolutionSerializer(solution)
        return Response(serializer.data, status.HTTP_200_OK)
    

class TeacherSolutionCreateView(APIView):
    permission_classes = [ AllowAny ]
    parser_classes = [ MultiPartParser ]

    def post(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE

        serializer = TeacherSolutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(question=question)
        return Response(serializer.data, status.HTTP_201_CREATED)