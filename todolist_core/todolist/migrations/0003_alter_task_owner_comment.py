# Generated by Django 5.1.4 on 2025-01-06 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_rename_title_task_name_task_owner_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='owner',
            field=models.CharField(default='admin', max_length=50, verbose_name='Владелец'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='todolist.task')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарий',
            },
        ),
    ]
