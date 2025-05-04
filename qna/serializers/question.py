from rest_framework import serializers
import os
from ..models.question import Question


class QuestionSerializer(serializers.ModelSerializer):
    content = serializers.CharField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'subject_category', 'image', 'content']


class QuestionImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        print(ext)
        if ext not in ['.png', '.jpg']:
            raise serializers.ValidationError('PNG, JPG 파일만 업로드할 수 있습니다')
        return value