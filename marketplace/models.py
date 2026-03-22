from django.db import models
from accounts.models import User

# Create your models here.
class Skill(models.Model):
  name = models.CharField(max_length=55)
  
  def __str__(self):
    return self.name

class FreelancerProfile(models.Model):
 user = models.OneToOneField(User, on_delete=models.CASCADE)
 skill = models.ManyToManyField(Skill, blank=True)
 
 def __str__(self):
  return self.user.username
