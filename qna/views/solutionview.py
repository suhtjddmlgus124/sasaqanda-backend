from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from ..models.question import Question
from ..models.solution import TeacherSolution, StudentSolution
from ..serializers.solution import TeacherSolutionSerializer, StudentSolutionSerializer

from utils.response import NOT_FOUND_RESPONSE, STAFF_ONLY_RESPONSE, AUTHOR_ONLY_RESPONSE, SUCCESS_RESPONSE


class TeacherSolutionRetrieveDestroyView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, solution_id):
        try:
            solution = TeacherSolution.objects.get(id=solution_id)
        except TeacherSolution.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = TeacherSolutionSerializer(solution)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, solution_id):
        user = request.user
        if user.role != 'STAFF':
            return STAFF_ONLY_RESPONSE
    
        try:
            solution = TeacherSolution.objects.get(id=solution_id)
        except TeacherSolution.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        solution.delete()
        return SUCCESS_RESPONSE
    

class TeacherSolutionListCreateView(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ MultiPartParser ]

    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        teacher_solutions = question.teacher_solutions
        serializer = TeacherSolutionSerializer(teacher_solutions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, question_id):
        user = request.user
        if user.role != 'STAFF':
            return STAFF_ONLY_RESPONSE

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE

        serializer = TeacherSolutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(question=question)
        return Response(serializer.data, status.HTTP_201_CREATED)
    

class StudentSolutionRetrieveDestroyView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, solution_id):
        try:
            solution = StudentSolution.objects.get(id=solution_id)
        except StudentSolution.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = StudentSolutionSerializer(solution)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, solution_id):
        try:
            solution = StudentSolution.objects.get(id=solution_id)
        except StudentSolution.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        user = request.user
        if solution.author != user and user.role != 'STAFF':
            return AUTHOR_ONLY_RESPONSE
        
        solution.delete()
        return SUCCESS_RESPONSE
    

class StudentSolutionListCreateView(APIView):
    permission_classes = [ IsAuthenticated ]
    parser_classes = [ MultiPartParser ]

    def get(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        student_solutions = question.student_solutions
        serializer = StudentSolutionSerializer(student_solutions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, question_id):
        user = request.user

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = StudentSolutionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(question=question, author=user)
        user.mastery += 1; user.save()
        return Response(serializer.data, status.HTTP_201_CREATED)