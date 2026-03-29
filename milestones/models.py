from django.db import models
from contracts.models import Contract
from accounts.models import User

# Create your models here.
class Milestone(models.Model):
  STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('submitted', 'Submitted'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
  )
  contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='milestones')
  title = models.CharField(max_length=55)
  amount = models.DecimalField(max_digits=12, decimal_places=2)
  order = models.IntegerField(default=1)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
  is_submitted = models.BooleanField(default=False)
  is_approved = models.BooleanField(default=False)
  
  def __str__(self):
    return self.title

class MilestoneSubmission(models.Model):
  milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name = 'submissions')
  submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'milest_submissions')
  submission_file = models.FileField(upload_to = 'milest_submissions/', blank=True, null=True)
  submitted_at = models.DateTimeField(auto_now_add=True)
  notes = models.TextField(blank=True, null=True)

  def __str__(self):
    return f'{self.milestone.title} by {self.submitted_by.username}'

class MilestoneReview(models.Model):
  submission = models.ForeignKey(MilestoneSubmission, on_delete=models.CASCADE, related_name = 'reviews')
  reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'milest_reviews')
  rating = models.PositiveIntegerField(blank=True, null=True)
  comments = models.TextField(blank=True, null=True)
  reviewed_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.submission.milestone.title

class MilestoneStatus(models.Model):
  milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name = 'miless_statuses')
  prev_status = models.CharField(max_length=50)
  new_status = models.CharField(max_length=50)
  changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name = 'milest_status_changes')
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.milestone.title
  
