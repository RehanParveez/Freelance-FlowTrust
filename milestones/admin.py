from django.contrib import admin
from milestones.models import Milestone, MilestoneSubmission, MilestoneReview, MilestoneStatus

# Register your models here.
@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
  list_display = ['contract', 'title', 'amount', 'status', 'is_submitted', 'is_approved']
    
@admin.register(MilestoneSubmission)
class MilestoneSubmissionAdmin(admin.ModelAdmin):
  list_display = ['milestone', 'submitted_by', 'submission_file', 'submitted_at', 'notes']

@admin.register(MilestoneReview)
class MilestoneReviewAdmin(admin.ModelAdmin):
  list_display = ['submission', 'reviewed_by', 'rating', 'comments', 'reviewed_at']
  
@admin.register(MilestoneStatus)
class MilestoneStatusAdmin(admin.ModelAdmin):
  list_display = ['milestone', 'prev_status', 'new_status', 'changed_by', 'date']