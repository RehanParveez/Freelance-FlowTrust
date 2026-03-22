from django.db import models
from accounts.models import User
from milestones.models import Milestone

# Create your models here.
class Wallet(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'wallet')
  balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
  
  def __str__(self):
    return self.user.username

class Escrow(models.Model):
  milestone = models.OneToOneField('milestones.Milestone', on_delete=models.CASCADE, related_name = 'escrow')
  client = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name = 'escrows_funded')
  freelancer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name = 'escrows_received')
  amount = models.DecimalField(max_digits=12, decimal_places=2)
  is_funded = models.BooleanField(default=False)
  is_released = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.amount} {self.is_funded}'

class Payment(models.Model):
  escrow = models.OneToOneField(Escrow, on_delete=models.CASCADE, related_name = 'payment')
  client = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'payments_done')
  freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'payments_received')
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.amount)
