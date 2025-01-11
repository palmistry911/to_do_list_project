from django.contrib import admin

from .models import Task, Comment


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'due_data')
    list_filter = ('status', 'owner', 'due_data')
    search_fields = ('name', 'description')

    inlines = [
        CommentInline,
    ]
