from django.db import models
from accounts.models import User
from contracts.models import Contract

class Talk(models.Model):
  participants = models.ManyToManyField(User, related_name = 'talks')
  contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, blank=True, related_name='talks')
  started_at = models.DateTimeField(auto_now_add=True)
  last_activity = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.id}'

class Message(models.Model):
    talk = models.ForeignKey(Talk, on_delete=models.CASCADE, related_name = 'messages')
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'messages_sent')
    content = models.TextField()
    read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'message {self.id} by {self.by.username}'

class Negotiation(models.Model):
  STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
  )
  contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name = 'negotiations')
  initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='negotiations_started')
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'negotiation {self.id} for {self.contract.title}'
