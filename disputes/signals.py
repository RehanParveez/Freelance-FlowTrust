from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dispute
from disputes.tasks import send_dispute_created
from disputes.disputes.cache_utils import cache_dispute

@receiver(post_save, sender=Dispute)
def dispute_created_signal(sender, instance, created, **kwargs):
  if created:
    cache_dispute(instance.id)
    send_dispute_created.delay(instance.id)