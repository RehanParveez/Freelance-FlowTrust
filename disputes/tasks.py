from celery import shared_task
from disputes.models import Dispute
from core.tasks import send_notification

@shared_task
def send_dispute_created(dispute_id):
  dispute = Dispute.objects.get(id=dispute_id)
  subject = 'the dispute is opened'
  message = f'the dispute is opened for the contract: {dispute.contract.title}'
  
  send_notification.delay(subject, message, dispute.contract.client.email)
  send_notification.delay(subject, message, dispute.contract.freelancer.email)
  
@shared_task
def periodic_dispute_reminders():
  unsolved_disputes = Dispute.objects.filter(status='open')
  for dispute in unsolved_disputes:
    send_notification.delay(dispute.id)
  