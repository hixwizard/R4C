from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def notify_customer(sender, instance, **kwargs):
    """Отправляет письмо, если робот появился в наличии."""
    orders = Order.objects.filter(robot_serial=instance.serial)
    message = f'''Недавно вы интересовались нашим роботом модели
              {instance.model}, версии {instance.version}.
              Этот робот теперь в наличии.
              Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.'''
    for order in orders:
        customer = order.customer
        return send_mail(
            'Добрый день!',
            message,
            'seller@rs.com',
            [customer.email],
            fail_silently=False,
        )
