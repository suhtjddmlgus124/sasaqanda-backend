from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from ..models.question import Question
from ..serializers.question import QuestionSerializer, QuestionImageSerializer
from utils.response import NOT_FOUND_RESPONSE, SUCCESS_RESPONSE, STAFF_ONLY_RESPONSE
import Levenshtein
from ..api import ocr


class QuestionRetrieveDestroyView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, question_id):
        user = request.user
        if user.role != 'STAFF':
            return STAFF_ONLY_RESPONSE

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        question.delete()
        return SUCCESS_RESPONSE


class QuestionCreateView(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        new_question = Question(**serializer.validated_data)
        new_question.get_content()
        new_question.get_vector()
        new_question.save()
        return Response(QuestionSerializer(new_question).data, status.HTTP_201_CREATED)


class QuestionSearchView(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        search = request.data.get('search')
        questions = Question.objects.all()
        questions_list = list(questions)
        sorted_questions = sorted(questions_list, key=lambda x: Levenshtein.ratio(x.content, search), reverse=True)
        serializer = QuestionSerializer(sorted_questions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class QuestionImageConvertView(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ MultiPartParser ]

    def post(self, request):
        user = request.user
        if user.token <= 0:
            return Response({'detail': '토큰이 부족합니다'}, status.HTTP_403_FORBIDDEN)

        serializer = QuestionImageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        image = serializer.validated_data.get('image')
        data = ocr.call_ocr_api(image.open("rb"))
        user.token -= 1; user.save()
        if data["status"] != 200:
            return Response({'detail': data["error"]}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({'content': data["text"]}, status.HTTP_200_OK)