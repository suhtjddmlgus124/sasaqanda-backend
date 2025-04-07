from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from ..models.question import Category
from ..serializers.question import CategorySerializer
from utils.response import NOT_FOUND_RESPONSE, SUCCESS_RESPONSE


class CategoryCreateRetrieveUpdateDestroyView(APIView):
    permission_classes = [ IsAdminUser ]

    def get(self, request, category_id):
        try:
            subject_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = CategorySerializer(subject_category)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, category_id):
        try:
            subject_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(parent=subject_category)
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def put(self, request, category_id):
        try:
            subject_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = CategorySerializer(subject_category, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, category_id):
        try:
            subject_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        subject_category.delete()
        return SUCCESS_RESPONSE