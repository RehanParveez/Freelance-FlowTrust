from rest_framework import serializers
from milestones.models import Milestone

class MilestoneSerializer(serializers.ModelSerializer):
  class Meta:
    model = Milestone
    fields = ['contract', 'title', 'amount', 'status', 'is_submitted', 'is_approved']