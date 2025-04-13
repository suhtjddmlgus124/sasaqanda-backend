from rest_framework import serializers
from ..models.question import Question


class QuestionSerializer(serializers.ModelSerializer):
    content = serializers.CharField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'subject_category', 'image', 'content']