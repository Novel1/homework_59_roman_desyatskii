from django.db import models
from django.utils import timezone

from webapp.models.project import Project


class Tracker(models.Model):
    summary = models.CharField(max_length=100, null=False, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    status = models.ManyToManyField(to='webapp.Status',
                                    related_name='tasks',
                                    blank=True)
    type = models.ManyToManyField(to='webapp.Type',
                                  related_name='type_tasks',
                                  blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(verbose_name='удалено', null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')
    deleted_at = models.DateTimeField(verbose_name='Дата и время удаления', null=True, default=None)

    def __str__(self):
        return f'{self.summary} - {self.description} - {self.type} - {self.status}'

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
