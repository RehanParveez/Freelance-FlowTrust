from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  CONTROL_CHOICES = (
    ('client', 'Client'),
    ('freelancer', 'Freelancer'),
    ('admin', 'Admin'),
  )
  email = models.EmailField(unique=True)
  phone = models.CharField(max_length=25)
  dob = models.DateField(null=True, blank=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  control = models.CharField(max_length=45, choices=CONTROL_CHOICES, default = 'client')
  date_joined = models.DateTimeField(auto_now_add=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
    
  def __str__(self):
    return f'{self.username} {self.control}'
  
class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'profile')
  bio = models.TextField(blank=True, null=True)
  pic = models.ImageField(upload_to = 'profiles/', blank=True, null=True)
  location = models.CharField(max_length=50, blank=True, null=True)
  
  def __str__(self):
    return self.user.username

class VerificationStatus(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'ver_status')
  is_verified = models.BooleanField(default=False)
  verified_at = models.DateTimeField(blank=True, null=True)
  
  def __str__(self):
    return f'{self.user.username} verified {self.is_verified}'
  
