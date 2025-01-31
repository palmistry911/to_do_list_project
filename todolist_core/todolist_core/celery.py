import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todolist_core.settings')

# Создаем экземпляр Celery
app = Celery(
    'todolist_core',
    broker_connection_retry=False,
    broker_connection_retry_on_startup=True,
)

# Загружаем настройки из файла Django
app.config_from_object(
    'django.conf:settings',
    namespace='CELERY')

# Автоматически обнаруживаем задачи в приложениях Django
app.autodiscover_tasks()

# Добавляем планировщик задач
# crontab(),  # Выполняется каждую минуту.
# crontab(minute='*/5'),  # Выполняется каждые 5 минут.
# crontab(hour=0, minute=0),  # Запуск каждый день в полночь
app.conf.beat_schedule = {
    'check_task_deadlines_daily': {
        'task': 'todolist.tasks.check_task_deadlines',
        'schedule': crontab(minute='*/5'),  # Выполняется каждые 5 минут.
    },
}
