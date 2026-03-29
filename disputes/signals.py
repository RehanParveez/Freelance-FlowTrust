from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dispute
from disputes.tasks import send_dispute_created
from disputes.disputes.cache_utils import cache_dispute
from accounts.accounts.cache_utils import cache_dashboard

@receiver(post_save, sender=Dispute)
def dispute_created_signal(sender, instance, created, **kwargs):
  if created:
    cache_dispute(instance.id)
    cache_dashboard(instance.contract.client.id)
    cache_dashboard(instance.contract.freelancer.id)
    send_dispute_created.delay(instance.id)