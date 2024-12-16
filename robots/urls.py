from django.urls import path

from .views import RobotCreate, Report

urlpatterns = [
    path('robot_create/', RobotCreate.as_view(), name='robot_create'),
    path('get_csv/', Report.as_view(), name='get_csv'),
]
