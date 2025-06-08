from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from ..models.question import Question
from ..models.solution import TeacherSolution, StudentSolution
from ..serializers.solution import TeacherSolutionSerializer, StudentSolutionSerializer
from utils.response import STAFF_ONLY_RESPONSE, AUTHOR_ONLY_RESPONSE, SUCCESS_RESPONSE


class TeacherSolutionRetrieveDestroyView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, solution_id):
        solution = get_object_or_404(TeacherSolution, id=solution_id)
        serializer = TeacherSolutionSerializer(solution)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, solution_id):
        user = request.user
        if user.role != 'STAFF':
            return STAFF_ONLY_RESPONSE
    
        solution = get_object_or_404(TeacherSolution, id=solution_id)
        solution.delete()
        return SUCCESS_RESPONSE
    

class TeacherSolutionListCreateView(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ MultiPartParser ]

    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        teacher_solutions = question.teacher_solutions
        serializer = TeacherSolutionSerializer(teacher_solutions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, question_id):
        user = request.user
        if user.role != 'STAFF':
            return STAFF_ONLY_RESPONSE

        question = get_object_or_404(Question, id=question_id)
        serializer = TeacherSolutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(question=question)
        return Response(serializer.data, status.HTTP_201_CREATED)
    

class StudentSolutionRetrieveDestroyView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, solution_id):
        solution = get_object_or_404(StudentSolution, id=solution_id)
        serializer = StudentSolutionSerializer(solution)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, solution_id):
        solution = get_object_or_404(StudentSolution, id=solution_id)

        user = request.user
        if solution.author != user and user.role != 'STAFF':
            return AUTHOR_ONLY_RESPONSE
        
        solution.delete()
        return SUCCESS_RESPONSE
    

class StudentSolutionListCreateView(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ MultiPartParser ]

    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        student_solutions = question.student_solutions
        serializer = StudentSolutionSerializer(student_solutions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, question_id):
        user = request.user

        question = get_object_or_404(Question, id=question_id)
        serializer = StudentSolutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(question=question, author=user)
        user.mastery += 1 
        user.token += 1
        user.save()
        return Response(serializer.data, status.HTTP_201_CREATED)