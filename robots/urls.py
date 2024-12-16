from django.urls import path

from .views import RobotCreate

urlpatterns = [
    path('robot_create/', RobotCreate.as_view(), name='robot_create')
]
