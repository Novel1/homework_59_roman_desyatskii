from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=60, verbose_name='Проект')
    description = models.TextField(max_length=3000, verbose_name='Описание')
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} - {self.description}'
