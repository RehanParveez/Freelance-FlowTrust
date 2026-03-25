# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import Payment
from core.tasks import send_notification

@receiver(post_save, sender=Payment)
def pay_released(sender, instance, created, **kwargs):
  if created:
    send_notification.delay(
      subject = 'the payment is released',
      message=f'{instance.amount}',
      recipient_email=instance.freelancer.email
    )