import re
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from .stables import STATUSES, COLORES


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')
    color = models.CharField(choices=COLORES, default='GREEN', verbose_name='Цвет', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'todolist'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Task(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тема задачи')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')

    status = models.CharField(choices=STATUSES, default='DRAFT', verbose_name='Статус', max_length=10)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    is_active = models.BooleanField('is active', default=True)
    tags = models.CharField(max_length=255, verbose_name='Теги', blank=True)

    due_data = models.DateTimeField(null=True, blank=True, verbose_name='Сроки выполненения')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.tags:
            # Разделение строки с тегами по запятым
            tag_names = [tag_name.strip() for tag_name in self.tags.split(',')]

            # Удаление пустых строк и дубликатов
            tag_names = list(set(filter(None, tag_names)))

            # Валидация тегов
            for tag_name in tag_names:
                self.validate_tag(tag_name)

            # Привязка тегов к задаче
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.task_tags.get_or_create(tag=tag)

    def validate_tag(self, tag_name):
        # Проверка длины тега
        if len(tag_name) > 50:
            raise ValidationError(f"Тег '{tag_name}' превышает допустимую длину в 50 символов.")

        # Проверка на недопустимые символы
        if not re.match(r'^[\w\s]+$', tag_name):
            raise ValidationError(f"Тег '{tag_name}' содержит недопустимые символы.")

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'todolist'
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')

    comment = models.CharField(max_length=255, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        app_label = 'todolist'
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарий'

    def __str__(self):
        return self.comment


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название тега', unique=True)

    class Meta:
        app_label = 'todolist'
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class TaskTag(models.Model):
    task = models.ForeignKey(Task, related_name='task_tags', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='task_tags', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task.name} - {self.tag.name}'
