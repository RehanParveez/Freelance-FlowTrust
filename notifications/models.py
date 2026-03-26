from django.db import models
from accounts.models import User

class Notification(models.Model):
  EVENT_CHOICES = (
    ('milest_submitt', 'Milest Submitt'),
    ('pay_released', 'Pay Released'),
    ('disp_created', 'Disp Created'),
    ('mess_received', 'Mess Received'),
    ('revi_posted', 'Revi Posted'),
   )
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='notifications')
  content = models.TextField()
  event_type = models.CharField(max_length=50, choices=EVENT_CHOICES, default = 'milest_submitt')
  read = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'notification {self.id} for {self.user.username}'

