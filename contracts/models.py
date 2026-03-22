from django.db import models
from accounts.models import User

# Create your models here.
class Contract(models.Model):
  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('active', 'Active'),
    ('completed', 'Completed'),
  )
  client = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'client_contracts')
  freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'freelancer_contracts')
  title = models.CharField(max_length=50)
  description = models.TextField(blank=True) 
  total_amount = models.DecimalField(max_digits=12, decimal_places=2)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title
