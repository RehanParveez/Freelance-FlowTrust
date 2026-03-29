from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from disputes.models import Dispute
from django.utils import timezone
from datetime import timedelta
from accounts.models import User

@shared_task
def send_notification(subject, message, recipient_email):
 send_mail(
  subject=subject,
  message=message,
  from_email=settings.EMAIL_HOST_USER,
  recipient_list=[recipient_email],
  fail_silently=False,
 )

@shared_task
def send_dispute_created(dispute_id=None):
  if dispute_id:
    disputes = Dispute.objects.filter(id=dispute_id)
    print(f'specific dispute id: {dispute_id}')
  else:
    disputes = Dispute.objects.filter(status='open')
    print(f'for all open disputes count: {disputes.count()}')
    
  for dispute in disputes:
    subject = 'the dispute is opened'
    message = f'the dispute is opened for the contract: {dispute.contract.title}'
    print(f'email for dispute id: {dispute.id}, of contract: {dispute.contract.title}')
    
    send_notification.delay(subject, message, dispute.contract.client.email)
    send_notification.delay(subject, message, dispute.contract.freelancer.email)
  
@shared_task
def periodic_dispute_reminders():
  unsolved_disputes = Dispute.objects.filter(status='open', created_at__lte=timezone.now() - timedelta(minutes=5))
  print(f'count of unsolved disputes {unsolved_disputes.count()}')
  
  for dispute in unsolved_disputes:
    subject = 'Reminder: the dispute is still open'
    message = f'{dispute.contract.title} this is still unsolved.'
    print(f'reminder for dispute id: {dispute.id}, of contract: {dispute.contract.title}')
    
    send_notification.delay(subject, message, dispute.contract.client.email)
    send_notification.delay(subject, message, dispute.contract.freelancer.email)
    
@shared_task
def send_inactivity_alert():
  cutoff_date = timezone.now() - timedelta(minutes=5)
  inactive_users = User.objects.filter(last_login__lt=cutoff_date)
  print(f'the inactive users are{inactive_users.count()} inactive users')
  
  for user in inactive_users:
    subject = 'why you are not using FlowTrust!'
    message = 'You have not logged in for a while, kindly stay updated'
    print(f'sending the email to: {user.email}')
    send_notification.delay(subject, message, user.email)
  