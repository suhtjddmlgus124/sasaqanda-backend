from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models.question import Question
from ..serializers.question import QuestionSerializer
from utils.response import NOT_FOUND_RESPONSE, SUCCESS_RESPONSE


class QuestionRetrieveDeleteView(APIView):
    permission_classes = [ AllowAny ]

    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        question.delete()
        return SUCCESS_RESPONSE


class QuestionCreateView(APIView):
    permission_classes = [ AllowAny ]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        new_question = Question(**serializer.validated_data)
        new_question.get_content()
        new_question.save()
        return Response(QuestionSerializer(new_question).data, status.HTTP_201_CREATED)