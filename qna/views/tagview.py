from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models.tag import TagCategory, Tag
from ..serializers.tag import TagCategoryListSerializer, TagCategorySerializer, TagSerializer
from utils.permission import IsStaffUser
from utils.response import SUCCESS_RESPONSE


class TagCategoryListView(APIView):
    permission_classes = [ IsAuthenticated, IsStaffUser ]

    def get(self, request):
        tag_categories = TagCategory.objects.all()
        serializer = TagCategoryListSerializer(tag_categories, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TagCategoryCreateRetrieveUpdateDestroyView(APIView):
    permission_classes = [ IsAuthenticated, IsStaffUser ]

    def get(self, request, tag_category_id):
        tag_category = get_object_or_404(TagCategory, id=tag_category_id)
        serializer = TagCategorySerializer(tag_category)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request, tag_category_id):
        tag_category = get_object_or_404(TagCategory, id=tag_category_id)
        serializer = TagCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(parent=tag_category)
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def patch(self, request, tag_category_id):
        tag_category = get_object_or_404(TagCategory, id=tag_category_id)
        serializer = TagCategorySerializer(tag_category, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, tag_category_id):
        tag_category = get_object_or_404(TagCategory, id=tag_category_id)
        tag_category.delete()
        return SUCCESS_RESPONSE


class TagListView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TagCreateView(APIView):
    permission_classes = [ IsAuthenticated, IsStaffUser ]

    def post(self, request, tag_category_id):
        tag_category = get_object_or_404(TagCategory, id=tag_category_id)
        serializer = TagSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(tag_category=tag_category)
        return Response(serializer.data, status.HTTP_201_CREATED)


class TagRetrieveUpdateDeleteView(APIView):
    permission_classes = [ IsAuthenticated, IsStaffUser ]

    def get(self, request, tag_id):
        tag = get_object_or_404(Tag, id=tag_id)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def patch(self, request, tag_id):
        tag = get_object_or_404(Tag, id=tag_id)
        serializer = TagSerializer(tag, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, tag_id):
        tag = get_object_or_404(Tag, id=tag_id)
        tag.delete()
        return SUCCESS_RESPONSE