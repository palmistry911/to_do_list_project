from django.urls import path, include
from .apps import TodolistConfig
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TaskViewSet,
    CommentViewSet,
)

app_name = 'todolist'

urlpatterns = []

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns += router.urls
