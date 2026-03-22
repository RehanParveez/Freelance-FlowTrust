from django.db import models
from contracts.models import Contract

# Create your models here.
class Milestone(models.Model):
  STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('submitted', 'Submitted'),
    ('approved', 'Approved'),
  )
  contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='milestones')
  title = models.CharField(max_length=55)
  amount = models.DecimalField(max_digits=12, decimal_places=2)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
  is_submitted = models.BooleanField(default=False)
  is_approved = models.BooleanField(default=False)
  
  def __str__(self):
    return self.title
  
