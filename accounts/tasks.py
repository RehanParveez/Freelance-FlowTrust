from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from core.tasks import send_notification
from accounts.models import User

@shared_task
def send_inactivity_alert():
  cutoff_date = timezone.now() - timedelta(days=30)
  inactive_users = User.objects.filter(last_login__lt=cutoff_date)
  for user in inactive_users:
    subject = 'why you are not using FlowTrust!'
    message = 'You have not logged in for a while, lindly stay updates'
    send_notification.delay(subject, message, user.email)