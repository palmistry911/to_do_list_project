from celery import shared_task
import time

@shared_task
def add(x, y):
    return x + y

@shared_task
def long_task():
    time.sleep(10)  # Имитируем длительное выполнение
    return 'Task Completed'