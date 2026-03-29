from django.db.models.signals import post_save
from django.dispatch import receiver
from milestones.models import Milestone
from disputes.tasks import send_notification

@receiver(post_save, sender=Milestone)
def milest_submitted(sender, instance, created, **kwargs):
  if instance.status == 'submitted':
    send_notification.delay(
      subject='milest is submitted',
      message=f"'{instance.title}' is submitted",
      recipient_email=instance.contract.client.email)