from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Comment
from .tasks import check_and_filter_post


@receiver(post_save, sender=Comment)
def check_save_comment(sender, instance, created, **kwargs):
    if created:
        # Запуск задачи Celery для проверки нового комментария
        check_and_filter_post.delay(instance.id)


# Инвалидация кэша при добавлении или изменении комментария
@receiver(post_save, sender=Comment)
def invalidate_cache_on_save(sender, instance, **kwargs):
    # Инвалидация кэша пользователя, которому принадлежит задача комментария
    cache_key = f'comments_{instance.task.owner.id}'
    cache.delete(cache_key)


# Инвалидация кэша при удалении комментария
@receiver(post_delete, sender=Comment)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    # Инвалидация кэша пользователя, которому принадлежит задача комментария
    cache_key = f'comments_{instance.task.owner.id}'
    cache.delete(cache_key)