from rest_framework import serializers
import os
from ..models.question import Question
from ..models.tag import Tag


class QuestionSerializer(serializers.ModelSerializer):
    content = serializers.CharField(read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    
    class Meta:
        model = Question
        fields = ['id', 'subject_category', 'image', 'content', 'tags']

    def validate_image(self, value):
        ext = os.path.splitext(value.name)[-1].lower()
        if ext not in ['.png', '.jpg', '.jpeg']:
            raise serializers.ValidationError('PNG, JPG, JPEG 파일만 업로드할 수 있습니다')
        return value


class QuestionImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def validate_image(self, value):
        ext = os.path.splitext(value.name)[-1].lower()
        if ext not in ['.png', '.jpg', '.jpeg']:
            raise serializers.ValidationError('PNG, JPG, JPEG 파일만 업로드할 수 있습니다')
        return value