from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import render
from django import forms

from .forms import RobotForm


class RobotCreate(View):
    """Класс для создания объекта модели Robot."""

    def get(self, request):
        """Отображает форму для создания объекта."""
        form = RobotForm()
        return render(request, 'robot_create.html', {'form': form})

    def post(self, request):
        """Обрабатывает данные формы."""
        form = RobotForm(request.POST)
        if form.is_valid():
            try:
                form.cleaned_data
                robot = form.save()
                return JsonResponse(
                    {
                        "model": robot.model,
                        "version": robot.version,
                        "created": robot.created
                    },
                    status=201,
                    json_dumps_params={'ensure_ascii': False}
                )
            except forms.ValidationError as e:
                return JsonResponse(
                    {'ошибка': str(e)},
                    status=400,
                    json_dumps_params={'ensure_ascii': False}
                )
        return JsonResponse(
            {'ошибка': form.errors},
            status=400,
            json_dumps_params={'ensure_ascii': False}
        )
