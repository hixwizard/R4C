import tempfile
import csv
from datetime import timedelta
from itertools import groupby
from operator import attrgetter
from collections import Counter

from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.shortcuts import render
from django import forms

from .forms import RobotForm
from .models import Robot


class RobotCreate(View):
    """
    Класс для создания объекта модели Robot.

    Отключить или обойти csrf без формы у меня не получилось.
    """

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
                )
            except forms.ValidationError as e:
                return JsonResponse(
                    {'ошибка': str(e)},
                    status=400,
                )
        return JsonResponse(
            {'ошибка': form.errors},
            status=400,
        )


class Report(View):
    """Генерирует постраничный отчет за неделю в формате CSV."""

    def get(self, request):
        """
        Создаёт .csv файл и загружает
        в директорию для загрузок по умолчанию.
        """
        now = timezone.now()
        one_week_ago = now - timedelta(days=7)
        robots = Robot.objects.filter(
            created__gte=one_week_ago
        ).order_by('model', 'version')
        with tempfile.NamedTemporaryFile(
            mode='w+', delete=False, newline='', encoding='utf-8'
        ) as temp_file:
            writer = csv.writer(temp_file)
            for model, group in groupby(robots, key=attrgetter('model')):
                writer.writerow([f"Модель: {model}"])
                writer.writerow(["Версия", "Количество за неделю"])
                version_counts = Counter(robot.version for robot in group)
                writer.writerows(version_counts.items())
                writer.writerow([])
            temp_file.seek(0)
            response = HttpResponse(temp_file.read(), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="weekly_report.csv"' # noqa
        return response
