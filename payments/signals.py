from django.db.models.signals import post_save
from django.dispatch import receiver
from payments.models import Payment, Wallet
from disputes.tasks import send_notification
from accounts.models import User
from payments.payments.cache_utils import cache_wallet

@receiver(post_save, sender=Payment)
def pay_released(sender, instance, created, **kwargs):
  if created:
    send_notification.delay(
      subject = 'the payment is released',
      message=f'{instance.amount}',
      recipient_email=instance.freelancer.email)
    cache_wallet(instance.freelancer.id)

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
  if created:
    Wallet.objects.create(user=instance)
    cache_wallet(instance.id)