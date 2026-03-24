from rest_framework import serializers
from contracts.serializers.basic import ContractSerializer1
from milestones.serializers.basic import MilestoneSubmissionSerializer1, MilestoneReviewSerializer1, MilestoneStatusSerializer1
from payments.serializers.basic import EscrowSerializer1, PaymentSerializer1
from accounts.serializers.basic import UserSerializer1
from milestones.models import Milestone, MilestoneSubmission, MilestoneReview, MilestoneStatus

class MilestoneSerializer(serializers.ModelSerializer):
  contract = ContractSerializer1(read_only=True)
  submissions = MilestoneSubmissionSerializer1(many=True, read_only=True)
  miless_statuses = MilestoneStatusSerializer1(many=True, read_only=True)
  escrow = EscrowSerializer1(read_only=True)
  payment = PaymentSerializer1(read_only=True)
  class Meta:
    model = Milestone
    fields = ['contract', 'submissions', 'miless_statuses', 'escrow', 'payment', 'title', 'amount', 'status', 'is_submitted', 'is_approved']
    
class MilestoneSubmissionSerializer(serializers.ModelSerializer):
  submitted_by = UserSerializer1(read_only=True)
  reviews = MilestoneReviewSerializer1(many=True, read_only=True)
  class Meta:
    model = MilestoneSubmission
    fields = ['milestone', 'submitted_by', 'submission_file', 'submitted_at', 'notes']
    
class MilestoneReviewSerializer(serializers.ModelSerializer):
  reviewed_by = UserSerializer1(read_only=True)
  class Meta:
    model = MilestoneReview
    fields = ['submission', 'reviewed_by', 'rating', 'comments', 'reviewed_at']
    
class MilestoneStatusSerializer(serializers.ModelSerializer):
  changed_by = UserSerializer1(read_only=True)
  class Meta:
    model = MilestoneStatus
    fields = ['milestone', 'prev_status', 'new_status', 'changed_by', 'date']