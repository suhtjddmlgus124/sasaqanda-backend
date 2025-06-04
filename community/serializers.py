from rest_framework import serializers
from django.utils import timezone
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'created_at', 'is_show']

    def get_created_at(self, obj):
        local_datetime = timezone.localtime(obj.created_at)
        formatted = local_datetime.strftime("%Y년 %m월 %d일 %p %I시 %M분")
        formatted = formatted.replace("AM", "오전").replace("PM", "오후")
        return formatted