from django.shortcuts import render
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .models import Task, Comment, Tag, Category
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    TaskSerializer,
)
from .permissions import IsAdminUser, IsOwner


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]


class TaskViewSet(viewsets.ModelViewSet):
    # queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        task = self.get_object()
        if task.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этой задачи.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этой задачи.")
        # instance.delete()
        instance.is_active = False
        instance.save()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cache_key = f'comments_{user.id}'
        comments = cache.get(cache_key)

        if not comments:
            # Возвращаем только те комментарии, которые принадлежат задачам текущего пользователя
            comments = Comment.objects.filter(task__owner=self.request.user)
            cache.set(cache_key, comments, timeout=60 * 5)  # Кешируем на 5 минут

        return comments

    @method_decorator(cache_page(60 * 15))  # Кешируем на уровне представления на 15 минут
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        if task.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этой задачи.")
        serializer.save()

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.task.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этой задачи.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.task.owner != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем этой задачи.")
        instance.delete()
