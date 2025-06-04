from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models.subject import SubjectCategory
from ..serializers.subject import SubjectCategorySerializer
from utils.permission import IsStaffUser
from utils.response import SUCCESS_RESPONSE


class SubjectCategoryCreateRetrieveUpdateDestroyView(APIView):
    permission_classes = [ IsAuthenticated, IsStaffUser ]

    def get(self, request, subject_category_id):
        subject_category = get_object_or_404(SubjectCategory, id=subject_category_id)
        serializer = SubjectCategorySerializer(subject_category)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, subject_category_id):
        subject_category = get_object_or_404(SubjectCategory, id=subject_category_id)
        serializer = SubjectCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(parent=subject_category)
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def patch(self, request, subject_category_id):
        subject_category = get_object_or_404(SubjectCategory, id=subject_category_id)        
        serializer = SubjectCategorySerializer(subject_category, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, subject_category_id):
        subject_category = get_object_or_404(SubjectCategory, id=subject_category_id)
        subject_category.delete()
        return SUCCESS_RESPONSE

