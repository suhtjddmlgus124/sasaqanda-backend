from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.question import SubjectCategory, Question
from ..serializers.question import SubjectCategorySerializer, QuestionSerializer
from utils.response import NOT_FOUND_RESPONSE








class QuestionRetrieveView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status.HTTP_200_OK)