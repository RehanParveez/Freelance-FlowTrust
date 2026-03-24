from rest_framework import serializers
from milestones.models import Milestone, MilestoneSubmission, MilestoneReview, MilestoneStatus

class MilestoneSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Milestone
    fields = ['contract', 'title', 'amount']
    read_only_fields = ['contract']
    
class MilestoneSubmissionSerializer1(serializers.ModelSerializer):
  class Meta:
    model = MilestoneSubmission
    fields = ['milestone', 'submitted_by']
    
class MilestoneReviewSerializer1(serializers.ModelSerializer):
  class Meta:
    model = MilestoneReview
    fields = ['submission', 'reviewed_by']
    
class MilestoneStatusSerializer1(serializers.ModelSerializer):
  class Meta:
    model = MilestoneStatus
    fields = ['milestone', 'prev_status']