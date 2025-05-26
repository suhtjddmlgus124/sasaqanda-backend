from rest_framework import serializers
from ..models.solution import TeacherSolution, StudentSolution
from accounts.serializers import UserIdentitySerializer
import os


class TeacherSolutionSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = TeacherSolution
        fields = ['id', 'question', 'image']

    def get_question(self, obj):
        return {'id': obj.question.id, 'image': obj.question.image.url}
    
    def validate_image(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in ['.png', '.jpg']:
            raise serializers.ValidationError('PNG, JPG 파일만 업로드할 수 있습니다')
        return value


class StudentSolutionSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    author = UserIdentitySerializer(required=False)

    class Meta:
        model = StudentSolution
        fields = ['id', 'question', 'image', 'author']

    def get_question(self, obj):
        return {'id': obj.question.id, 'image': obj.question.image.url}
    
    def validate_image(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in ['.png', '.jpg']:
            raise serializers.ValidationError('PNG, JPG 파일만 업로드할 수 있습니다')
        return value