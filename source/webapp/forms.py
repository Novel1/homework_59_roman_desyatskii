from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from webapp.models import Tracker

from webapp.models.project import Project


class TrackerForm(forms.ModelForm):
    summary = forms.CharField(max_length=30, validators=(MinLengthValidator(limit_value=2,
                                                                            message='Кратокое описание должно быть больше 1 символа'),))

    class Meta:

        model = Tracker
        fields = ('summary', 'description', 'status', 'type')
        labels = {
            'summary': 'Краткое описание',
            'description': 'Описание',
            'status': 'Cтатус',
            'type': 'Тип',
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise ValidationError('Описание должено быть длиннее 10 символов')
        elif len(description) > 150:
            raise ValidationError('Описание должено быть меньше 150 символов')
        return description


class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False, label='Найти')


class ProjectForm(forms.ModelForm):
    class Meta:

        model = Project
        fields = ('name', 'description', 'start_date', 'end_date')
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'start_date': 'Дата начало',
            'end_date': 'Дата конца',
        }