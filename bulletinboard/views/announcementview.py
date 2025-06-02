from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Announcement
from ..serializers import AnnouncementSerializer


class AnnouncementListCreateView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        announcements = Announcement.objects.filter(is_show=True)
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AnnouncementSerializer(request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class AnnouncementRetrieveView(APIView):
    permission_classes = [ IsAuthenticated ]
    
    @staticmethod
    def get_announcement_or_404(id):
        announcement = get_object_or_404(Announcement, id=id, is_show=True)
        return announcement
    
    def get(self, request, announcement_id):
        announcement = self.get_announcement_or_404(announcement_id)
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data, status.HTTP_200_OK)
    