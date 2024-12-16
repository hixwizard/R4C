from django import forms
from datetime import datetime as dt

from .models import Robot


class RobotForm(forms.ModelForm):

    """Форма для создания объекта Robot."""

    class Meta:
        model = Robot
        fields = ('model', 'version', 'created')

    def validate_field(self, value: str):
        """Общая проверка для model и version."""
        return len(value) == 2 and value.isalnum() and value.isupper()

    def clean(self):
        """Метод для проверки всех данных формы."""
        cleaned_data = super().clean()
        model = cleaned_data.get('model')
        version = cleaned_data.get('version')
        created = cleaned_data.get('created')
        today = dt.today()
        if created < today:
            raise forms.ValidationError("Дата создания не валидна.")
        for field in [model, version]:
            if field and not self.validate_field(field):
                raise forms.ValidationError("Неверный формат модели/версии.")
        return cleaned_data
