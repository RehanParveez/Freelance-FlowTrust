from django.db.models.signals import post_save
from django.dispatch import receiver
from contracts.models import Contract
from analytics.utils import user_analytics, contract_analytics, earning_report
from milestones.models import Milestone
from payments.models import Payment

@receiver(post_save, sender=Contract)
def contract_created(sender, instance, created, **kwargs):
  if created:
    user_analytics(instance.client, 'total_contr')
    user_analytics(instance.freelancer, 'total_contr')
    print(f'the contr is for {instance.id}')

@receiver(post_save, sender=Contract)
def contract_completed(sender, instance, created, **kwargs):
  if not created and instance.status == 'completed':
    user_analytics(instance.client, 'completed_contr')
    user_analytics(instance.freelancer, 'completed_contr')
    print(f'its completed for {instance.id}')

@receiver(post_save, sender=Milestone)
def milestone_created(sender, instance, created, **kwargs):
  if created:
    contract_analytics(instance.contract, 'total_milest')
    print(f'the milest is for {instance.id}')

@receiver(post_save, sender=Milestone)
def milestone_approved(sender, instance, created, **kwargs):
  if not created and instance.status == 'approved':
    contract_analytics(instance.contract, 'milest_completed')
    print(f'the milest is appr for {instance.id}')

@receiver(post_save, sender=Payment)
def payment_created(sender, instance, created, **kwargs):
  if created:
    user_analytics(instance.freelancer, 'total_earnings', instance.amount)
    contract_analytics(instance.escrow.milestone.contract, 'total_pay', instance.amount)
    earning_report(instance.freelancer, instance.escrow.milestone.contract, instance.amount)
    print(f'the pay is for {instance.amount}')