from rest_framework import serializers
from ..models.question import SubjectCategory, TagCategory, Question, Tag


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = []


class SubjectCategorySerializer(serializers.ModelSerializer):
    breadcrum = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()

    class Meta:
        model = SubjectCategory
        fields = ['id', 'name', 'parent', 'subcategories', 'questions', 'breadcrumb']

    def get_breadcrumb(self, obj):
        ret = [{'id': obj.id, 'name': obj.name}]
        parent = obj.parent
        while parent:
            ret.insert(0, {'id': parent.id, 'name': parent.name})
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


class TagCategorySerializer(serializers.ModelSerializer):
    breadcrumb = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = TagCategory
        fields = ['id', 'name', 'parent', 'subcategories', 'tags', 'breadcrumb']

    def get_breadcrumb(self, obj):
        ret = [{'id': obj.id, 'name': obj.name}]
        parent = obj.parent
        while parent:
            ret.insert(0, {'id': parent.id, 'name': parent.name})
            parent = parent.parent
        return ret
    
    def get_subcategories(self, obj):
        ret = []
        for tag_category in obj.subcategories.all():
            ret.append({'id': tag_category.id, 'name': tag_category.name})
        return ret
    
    def get_tags(self, obj):
        ret = []
        for tag in obj.tags.all():
            ret.append({'id': tag.id, 'name': tag.name})
        return ret


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']