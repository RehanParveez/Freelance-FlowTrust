from django.db import models
from accounts.models import User
from milestones.models import Milestone

# Create your models here.
class Wallet(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'wallet')
  balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
  
  def __str__(self):
    return self.user.username

class Transaction(models.Model):
  TRANSACTION_CHOICES = (
    ('deposit', 'Deposit'),
    ('withdraw', 'Withdraw'),
    ('refund', 'Refund'),
  )
  wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name = 'transactions')
  amount = models.DecimalField(max_digits=12, decimal_places=2)
  transaction = models.CharField(max_length=50, choices=TRANSACTION_CHOICES, default = 'deposit')
  date = models.DateTimeField(auto_now_add=True)
  description = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.wallet.user.username

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

class Refund(models.Model):
  payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name = 'refunds')
  amount = models.DecimalField(max_digits=12, decimal_places=2)
  reason = models.TextField()
  refunded_at = models.DateTimeField(auto_now_add=True)

class PaymentMethod(models.Model):
  METHOD_CHOICES = (
    ('card', 'Card'),
    ('stripe', 'Stripe'),
    ('paypal', 'Paypal'),
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'pay_methods')
  method_type = models.CharField(max_length=50, choices=METHOD_CHOICES, default = 'card') 
  is_default = models.BooleanField(default=False)

  def __str__(self):
    return self.user.username

