from django.db import models
from accounts.models import User
from contracts.models import Contract

class UserAnalytics(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'analytics')
  total_contr = models.PositiveIntegerField(default=0)
  completed_contr = models.PositiveIntegerField(default=0)
  total_earnings = models.DecimalField(max_digits=12, decimal_places=2)

  def __str__(self):
    return f'{self.user.username}'

class EarningReport(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'earning_reports')
  contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'earning_reports')
  amount = models.DecimalField(max_digits=12, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'earnings {self.amount} for {self.user.username}'

class ContractAnalytics(models.Model):
  contract = models.OneToOneField(Contract, on_delete=models.CASCADE, related_name = 'analytics')
  total_milest = models.PositiveIntegerField(default=0)
  milest_completed = models.PositiveIntegerField(default=0)
  total_pay = models.DecimalField(max_digits=12, decimal_places=2)

  def __str__(self):
    return f'{self.contract.title}'
