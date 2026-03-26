from django.db import models
from accounts.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Contract(models.Model):
  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('completed', 'Completed'),
  )
  client = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'client_contracts')
  freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'freelancer_contracts')
  title = models.CharField(max_length=50)
  description = models.TextField(blank=True) 
  total_amount = models.DecimalField(max_digits=12, decimal_places=2)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default = 'pending')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title

class ContrParticipant(models.Model):
  ROLE_CHOICES = (
    ('client', 'Client'),
    ('freelancer', 'Freelancer'),
  )
  contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name = 'participants')
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'contract_participations')
  role = models.CharField(max_length=45, choices=ROLE_CHOICES, default='client')  

  def __str__(self):
    return f'{self.user.username} in {self.contract.title}'
  
class ContractTerm(models.Model):
  contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name = 'terms')
  description = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f'{self.contract.title}'

class ContractStatus(models.Model):
  contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name = 'contr_statuses')
  prev_status = models.CharField(max_length=60)
  new_status = models.CharField(max_length=60)
  changed_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name = 'contr_sta_chang')
  date = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.contract.title
  
class Activity(models.Model):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'activities')
  action_type = models.CharField(max_length=150)
  content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
  object_id = models.PositiveIntegerField(null=True)
  content_object = GenericForeignKey('content_type', 'object_id')
  date = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    ordering = ['-date']

  def __str__(self):
    return f'{self.user} {self.action_type} {self.date}'
  
