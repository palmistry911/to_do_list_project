from rest_framework import serializers
#from .utils import get_cached_tags
from .models import Task, Comment, Tag, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['task', 'comment']


class TaskSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(source='comments.all.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags_count = serializers.SerializerMethodField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'category', 'status', 'owner',
                  'tags', 'is_active', 'due_date', 'comments_count', 'comments'
                  ]
        read_only_fields = ['owner']

    def get_tags(self, obj):
        tags = get_cached_tags(obj.id)
        return [tag.name for tag in tags]
