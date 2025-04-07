from rest_framework import serializers
from ..models.solution import TeacherSolution, StudentSolution


class TeacherSolutionSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = TeacherSolution
        fields = ['id', 'question', 'image']

    def get_question(self, obj):
        return {'id': obj.question.id, 'image': obj.question.image}


class StudentSolutionSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = StudentSolution
        fields = ['id', 'question', 'image', 'author']

    def get_question(self, obj):
        return {'id': obj.question.id, 'image': obj.question.image}