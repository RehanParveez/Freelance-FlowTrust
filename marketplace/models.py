from django.db import models
from django.utils import timezone
from accounts.models import User

# Create your models here.
class Skill(models.Model):
  name = models.CharField(max_length=55)
  category = models.CharField(max_length=50, blank=True, null=True)
  created_at = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return self.name

class FreelancerProfile(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'freelancer_prof')
 skill = models.ManyToManyField(Skill, blank=True, related_name = 'freelancers')
 bio = models.TextField(blank=True, null=True)
 hour_rate = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
 portf_url = models.URLField(blank=True, null=True)
 
 def __str__(self):
  return self.user.username

class Portfolio(models.Model):
  freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name = 'portfolios')
  title = models.CharField(max_length=170)
  description = models.TextField(blank=True, null=True)
  link = models.URLField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
   return f'{self.title} {self.freelancer.user.username}'

class JobPost(models.Model):
  client = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'job_posts')
  name = models.CharField(max_length=50)
  description = models.TextField(blank=True, null=True)
  budget = models.DecimalField(max_digits=12, decimal_places=2)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.name

class Proposal(models.Model):
  job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name = 'proposals')
  freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE, related_name = 'proposals')
  proposed_amount  = models.DecimalField(max_digits=12, decimal_places=2)
  submitted_at = models.DateTimeField(auto_now_add=True)
  is_accepted = models.BooleanField(default=False)
  
  def __str__(self):
    return f'{self.freelancer.user.username} {self.job.name}'

