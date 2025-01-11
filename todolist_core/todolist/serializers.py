from rest_framework import serializers

from .models import Task, Comment, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['task', 'comment']


class TaskSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField(source='comments.all.count')
    comments = CommentSerializer(many=True, read_only=True)
    tags_count = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        exclude = ['owner']

    def get_tags_count(self, obj):
        return obj.tags.count()
