from django.db import models
from accounts.models import User
from contracts.models import Contract
from milestones.models import Milestone

class Dispute(models.Model):
  STATUS_CHOICES = (
    ('open', 'Open'),
    ('checking', 'Checking'),
    ('solved', 'Solved'),
    ('closed', 'Closed'),
  )
  contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name = 'disputes')
  milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, blank=True, null=True, related_name = 'disputes')
  raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'disputes_raised')
  description = models.TextField()
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default = 'open')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.id} {self.contract.title}'

class DisputeMessage(models.Model):
  dispute = models.ForeignKey(Dispute, on_delete=models.CASCADE, related_name = 'messages')
  by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'dispute_messages')
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.by.username}'

class Proof(models.Model):
  dispute = models.ForeignKey(Dispute, on_delete=models.CASCADE, related_name = 'proofs')
  file = models.FileField(upload_to = 'dispute_proofs/')
  description = models.TextField(blank=True, null=True)
  uploaded_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.id} {self.dispute.id}'

class Solution(models.Model):
  dispute = models.OneToOneField(Dispute, on_delete=models.CASCADE, related_name = 'solutions')
  decision = models.TextField()
  solved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'solutions_done')
  solved_at = models.DateTimeField(auto_now_add=True)
  amount_rel_to_freel = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
  amount_ref_to_client = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

  def __str__(self):
    return f'{self.dispute.id}'
