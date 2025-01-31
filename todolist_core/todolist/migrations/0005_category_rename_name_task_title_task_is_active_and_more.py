# Generated by Django 5.1.5 on 2025-01-30 21:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0004_tag_task_tags'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Категория')),
                ('color', models.CharField(choices=[('RED', 'Красный'), ('YELLOW', 'Желтый'), ('GREEN', 'Зеленый'), ('BLUE', 'Синий'), ('BLACK', 'Черный'), ('WHITE', 'Белый')], default='GREEN', max_length=10, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.RenameField(
            model_name='task',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='task',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название тега'),
        ),
        migrations.AlterField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.RemoveField(
            model_name='task',
            name='tags',
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='todolist.category', verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='TaskTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_tags', to='todolist.tag')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_tags', to='todolist.task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='tags',
            field=models.CharField(blank=True, max_length=255, verbose_name='Теги'),
        ),
    ]
