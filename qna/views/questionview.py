from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from ..models.question import Question
from ..serializers.question import QuestionSerializer, QuestionImageSerializer
from utils.response import SUCCESS_RESPONSE, STAFF_ONLY_RESPONSE
import Levenshtein
from sklearn.metrics.pairwise import cosine_similarity
from ..api import ocr, gpt


class QuestionRetrieveDestroyView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, question_id):
        user = request.user
        if user.role != 'STAFF':
            return STAFF_ONLY_RESPONSE

        question = get_object_or_404(Question, id=question_id)
        question.delete()
        return SUCCESS_RESPONSE


class QuestionCreateView(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ MultiPartParser ]

    def post(self, request):
        user = request.user
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        tags = validated_data.pop('tags', [])
        
        new_question = Question(**serializer.validated_data)
        new_question.get_content()
        new_question.get_vector()
        new_question.save()
        new_question.tags.set(tags)
        user.mastery += 1
        user.save()
        return Response(QuestionSerializer(new_question).data, status.HTTP_201_CREATED)


class QuestionSearchView(APIView):
    permission_classes = [ IsAuthenticated ]

    def post(self, request):
        HIGHEST_ACCURATE_QUESTION_COUNT = 7
        # WEIGHT_COEFFICIENT = 1.2

        search = request.data.get('search')
        tags = request.data.get('tags')
        method = request.data.get('method', 'edit')

        if tags:
            questions = Question.objects.annotate(
                matched_tags=Count('tags', filter=Q(tags__name__in=tags), distinct=True), 
                total_tags=Count('tags', distinct=True)
            ).filter(
                matched_tags=len(tags),
            )
        else:
            questions = Question.objects.all()

        # calculated_list = [(q, Levenshtein.ratio(q.content, search)) for q in questions]
        # sorted_list = sorted(calculated_list, key=lambda x: x[1], reverse=True)[:HIGHEST_ACCURATE_QUESTION_COUNT]
        # average_accuracy = sum([x[1] for x in sorted_list])/HIGHEST_ACCURATE_QUESTION_COUNT
        # filtered_list = filter(lambda x: x[1] >= average_accuracy*WEIGHT_COEFFICIENT, sorted_list)
        # filtered_questions = [x[0] for x in filtered_list]


        if method == 'edit':
            sorted_list = sorted(questions, key=lambda q: Levenshtein.ratio(q.content, search), reverse=True)[:HIGHEST_ACCURATE_QUESTION_COUNT]

        elif method == 'gpt':
            search_vector = gpt.call_gpt_api(search)
            sorted_list = sorted(questions, key=lambda q: cosine_similarity([q.vector], [search_vector]), reverse=True)[:HIGHEST_ACCURATE_QUESTION_COUNT]

        serializer = QuestionSerializer(sorted_list, many=True)
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
        if not data["success"]:
            return Response({'detail': data["error"]}, status.HTTP_400_BAD_REQUEST)
        
        return Response({'content': data["text"]}, status.HTTP_200_OK)