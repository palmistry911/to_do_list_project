from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Task, Tag, Comment


class TaskTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Initial Title", description="Initial Description")

    def test_create_task(self):
        response = self.client.get(
            reverse('todolist: create'),
        data = {"title”: 'Test Task', “description”: 'Test Description"}
        )
        self.assertEqual(response.status_code, 200)
        task = Task.objects.all().first()
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")

    def test_edit_task(self):
        self.task.title = "Updated Title"
        self.task.save()
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.title, "Updated Title")

    def test_view_task(self):
        task = Task.objects.get(id=self.task.id)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")


class TaskIntegrationTestCase(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title="Test Task", description="Test Description")

    def test_add_comment_to_task(self):
        comment = Comment.objects.create(task=self.task, text="Test Comment")
        self.task.refresh_from_db()
        self.assertIn(comment, self.task.comments.all())

    def test_add_tags_to_task(self):
        self.task.tags.add(self.tag)
        self.task.refresh_from_db()
        self.assertIn(self.tag, self.task.tags.all())
