from rest_framework import serializers
from ..models.subject import SubjectCategory


class SubjectCategorySerializer(serializers.ModelSerializer):
    breadcrumb = serializers.SerializerMethodField()
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