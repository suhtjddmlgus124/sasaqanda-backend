from rest_framework import serializers
from ..models.question import Category, Question, Tag


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = []


class CategorySerializer(serializers.ModelSerializer):
    breadcrum = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'subcategories', 'questions', 'breadcrum']

    def get_breadcrum(self, obj):
        ret = [{'id': obj.id, 'name': obj.name}]
        parent = obj.parent
        while parent:
            ret.insert(0, {'id':parent.id, 'name':parent.name})
            parent = parent.parent
        return ret
    
    def get_subcategories(self, obj):
        ret = []
        for category in obj.subcategories.all():
            ret.append({'id': category.id, 'name': category.name})
        return ret
    
    def get_questions(self, obj):
        ret = []
        for question in obj.questions.all():
            ret.append({'id': question.id})
        return ret


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']