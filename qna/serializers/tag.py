from rest_framework import serializers
from ..models.tag import TagCategory, Tag


class TagCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagCategory
        fields = ['id', 'name']

class TagCategorySerializer(serializers.ModelSerializer):
    breadcrumb = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = TagCategory
        fields = ['id', 'name', 'parent', 'subcategories', 'tags', 'breadcrumb']

    def validate_parent(self, value):
        if value == self.instance:
            raise serializers.ValidationError("parent는 자신이 될 수 없습니다")
        return value

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
        fields = ['id', 'name', 'tag_category']