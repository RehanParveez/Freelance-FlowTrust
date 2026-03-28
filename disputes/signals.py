from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dispute
from disputes.tasks import send_dispute_created

@receiver(post_save, sender=Dispute)
def dispute_created_signal(sender, instance, created, **kwargs):
  if created:
    send_dispute_created.delay(instance.id)