import re
from django.db import transaction

from todolist_core.celery import app
from .models import Comment, Task
from .stables import BANNED_WORDS, BANNED_REPLACE
from datetime import datetime, timedelta
from django.utils import timezone

# @shared_task
@app.task
def check_and_filter_post(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        original_text = comment.comment
        filtered_text = original_text

        # Используем регулярные выражения для замены всех вхождений запрещенных слов
        for word in BANNED_WORDS:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            filtered_text = pattern.sub(BANNED_REPLACE, filtered_text)

        # Если текст изменился, сохраняем комментарий
        if filtered_text != original_text:
            with transaction.atomic():
                comment.comment = filtered_text
                comment.save()

        return f"Replacing '{original_text}' with '{filtered_text}'."

    except Comment.DoesNotExist:
        pass

@app.task
def check_task_deadlines():
    # Получаем текущую дату
    today = timezone.now().date()

    # Получаем все задачи, у которых дедлайн сегодня или прошел
    overdue_tasks = Task.objects.filter(due_date__lte=today, is_active=True, status='PUBLISHED')

    # Сдвигаем дедлайн на один день вперед для всех найденных задач
    for task in overdue_tasks:
        task.due_date = task.due_date + timedelta(days=1)
        task.save()

    return f"Updated {overdue_tasks.count()} tasks."