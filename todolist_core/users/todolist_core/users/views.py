from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .permissions import IsOwner
from django.http import JsonResponse
from .tasks import add,long_task


def add_view(request):
    result = add.delay(4, 4) # вызов асинхронной задачи
    return JsonResponse({'task_id': result.id, 'status': 'Task Submitted'})

def long_task_view(request):
    result = long_task.delay() # вызов асинхронной задачи
    return JsonResponse({'task_id': result.id, 'status': 'Long Task Submitted'})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ToDoListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
