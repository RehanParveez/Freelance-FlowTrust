from django.db import models
from accounts.models import User
from contracts.models import Contract
from milestones.models import MilestoneSubmission

class Review(models.Model):
  reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'reviews_given')
  reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'reviews_got')
  contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'reviewss')
  milest_submiss = models.ForeignKey(MilestoneSubmission, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'reviewss')
  comments = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'review {self.id} by {self.reviewer.username}'

class Rating(models.Model):
  review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name = 'rating')
  score = models.PositiveIntegerField()
  quality = models.PositiveIntegerField(blank=True, null=True)
  professionalism = models.PositiveIntegerField(blank=True, null=True)

  def __str__(self):
    return f'rating {self.score} for review {self.review.id}'
