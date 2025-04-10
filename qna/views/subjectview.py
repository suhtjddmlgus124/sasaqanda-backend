from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.subject import SubjectCategory
from ..serializers.subject import SubjectCategorySerializer
from utils.permission import IsStaffUser
from utils.response import NOT_FOUND_RESPONSE, SUCCESS_RESPONSE


class SubjectCategoryCreateRetrieveUpdateDestroyView(APIView):
    permission_classes = [ IsAuthenticated, IsStaffUser ]

    def get(self, request, subject_category_id):
        try:
            subject_category = SubjectCategory.objects.get(id=subject_category_id)
        except SubjectCategory.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = SubjectCategorySerializer(subject_category)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, subject_category_id):
        try:
            subject_category = SubjectCategory.objects.get(id=subject_category_id)
        except SubjectCategory.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = SubjectCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(parent=subject_category)
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def put(self, request, subject_category_id):
        try:
            subject_category = SubjectCategory.objects.get(id=subject_category_id)
        except SubjectCategory.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = SubjectCategorySerializer(subject_category, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, subject_category_id):
        try:
            subject_category = SubjectCategory.objects.get(id=subject_category_id)
        except SubjectCategory.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        subject_category.delete()
        return SUCCESS_RESPONSE

