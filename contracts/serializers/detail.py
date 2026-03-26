from rest_framework import serializers
from accounts.serializers.basic import UserSerializer1
from milestones.serializers.basic import MilestoneSerializer1
from contracts.serializers.basic import ContrParticipantSerializer1, ContractTermSerializer1
from contracts.serializers.basic import ContractStatusSerializer1
from contracts.models import Contract, ContrParticipant, ContractTerm, ContractStatus, Activity
from disputes.serializers.basic import DisputeSerializer1
from communication.serializers.basic import NegotiationSerializer1
from reviews.serializers.basic import ReviewSerializer1
from accounts.models import User

class ContractSerializer(serializers.ModelSerializer):
  client = UserSerializer1(read_only=True)
  freelancer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
  freela_detail = UserSerializer1(source = 'freelancer', read_only=True)
  milestones = MilestoneSerializer1(many=True, read_only=True)
  participants = ContrParticipantSerializer1(many=True, read_only=True)
  terms = ContractTermSerializer1(many=True, read_only=True)
  contr_statuses = ContractStatusSerializer1(many=True, read_only=True)
  disputes = DisputeSerializer1(many=True, read_only=True)
  negotiations = NegotiationSerializer1(many=True, read_only=True)
  reviews = ReviewSerializer1(many=True, read_only=True)
  class Meta:
    model = Contract
    fields = ['client', 'freelancer', 'freela_detail', 'milestones', 'participants', 'terms', 'contr_statuses', 'disputes', 'negotiations', 'reviews', 'title', 'description', 'total_amount', 'status', 'created_at']
    
class ContrParticipantSerializer(serializers.ModelSerializer):
  user = UserSerializer1(read_only=True)
  class Meta:
    model = ContrParticipant
    fields = ['contract', 'user', 'role']
    
class ContractTermSerializer(serializers.ModelSerializer):
  class Meta:
    model = ContractTerm
    fields = ['contract', 'description', 'created_at']
    
class ContractStatusSerializer(serializers.ModelSerializer):
  changed_by = UserSerializer1(read_only=True)
  class Meta:
    model = ContractStatus
    fields = ['contract', 'prev_status', 'new_status', 'changed_by', 'date']
    
class ActivitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Activity
    fields = ['user', 'action_type', 'content_type', 'object_id', 'content_object', 'date']