from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..models.tag import TagCategory, Tag
from ..serializers.tag import TagCategoryListSerializer, TagCategorySerializer
from utils.permission import IsStaffUser
from utils.response import NOT_FOUND_RESPONSE, SUCCESS_RESPONSE


class TagCategoryListView(APIView):
    permission_classes = [ IsAuthenticated, IsStaffUser ]

    def get(self, request):
        tag_categories = TagCategory.objects.all()
        serializer = TagCategoryListSerializer(tag_categories, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TagCategoryCreateRetrieveUpdateDestroyView(APIView):
    permission_classes = [ IsAuthenticated, IsStaffUser ]

    def get(self, request, tag_category_id):
        try:
            tag_category = TagCategory.objects.get(id=tag_category_id)
        except TagCategory.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = TagCategorySerializer(tag_category)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, tag_category_id):
        try:
            tag_category = TagCategory.objects.get(id=tag_category_id)
        except TagCategory.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = TagCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(parent=tag_category)
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def patch(self, request, tag_category_id):
        try:
            tag_category = TagCategory.objects.get(id=tag_category_id)
        except TagCategory.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        serializer = TagCategorySerializer(tag_category, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, tag_category_id):
        try:
            tag_category = TagCategory.objects.get(id=tag_category_id)
        except TagCategory.DoesNotExist:
            return NOT_FOUND_RESPONSE
        
        tag_category.delete()
        return SUCCESS_RESPONSE