from django.contrib import admin

from customers.models import Customer
from orders.models import Order
from .models import Robot


class RobotAdmin(admin.ModelAdmin):
    list_display = (
        'serial',
        'model',
        'version',
        'created'
    )


admin.site.register(Robot)
admin.site.register(Order)
admin.site.register(Customer)
