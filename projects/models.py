from django.conf import settings
from django.db import models

from projects.identifiers import (
    STATE_LABEL_LIMIT,
    VENTURE_TITLE_LIMIT,
)


class Project(models.Model):
    """Модель проекта"""

    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_CLOSED, 'Closed'),
    ]

    name = models.CharField(
        max_length=VENTURE_TITLE_LIMIT,
        verbose_name='Название проекта'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание проекта'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Автор'
    )
    github_url = models.URLField(
        blank=True,
        verbose_name='Ссылка на GitHub'
    )
    status = models.CharField(
        max_length=STATE_LABEL_LIMIT,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
