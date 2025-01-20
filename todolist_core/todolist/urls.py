from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TagViewSet, CommentListCreateAPIView, CommentRetrieveUpdateDestroyAPIView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'tags', TagViewSet)

app_name = 'todolist'

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', CommentListCreateAPIView.as_view()),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view()),
]
