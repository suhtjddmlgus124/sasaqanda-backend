from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Topic
from ..serializers import TopicSerializer
from utils.response import AUTHOR_ONLY_RESPONSE, SUCCESS_RESPONSE


class TopicListCreateView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        topics = Topic.objects.order_by('-created_at')
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        serializer = TopicSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save(author=user)
        return Response(serializer.data, status.HTTP_201_CREATED)
    

class TopicRetrieveUpdateDestroyView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, id=topic_id)
        serializer = TopicSerializer(topic)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def patch(self, request, topic_id):
        user = request.user
        topic = get_object_or_404(Topic, id=topic_id)
        if topic.author != user:
            return AUTHOR_ONLY_RESPONSE
        
        serializer = TopicSerializer(topic, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    
    def delete(self, request, topic_id):
        user = request.user
        topic = get_object_or_404(Topic, id=topic_id)
        if topic.author != user and user.role != 'STAFF':
            return AUTHOR_ONLY_RESPONSE
        
        topic.delete()
        return SUCCESS_RESPONSE