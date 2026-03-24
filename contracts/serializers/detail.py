from rest_framework import serializers
from accounts.serializers.basic import UserSerializer1
from milestones.serializers.basic import MilestoneSerializer1
from contracts.serializers.basic import ContrParticipantSerializer1, ContractTermSerializer1
from contracts.serializers.basic import ContractStatusSerializer1
from contracts.models import Contract, ContrParticipant, ContractTerm, ContractStatus

class ContractSerializer(serializers.ModelSerializer):
  client = UserSerializer1(read_only=True)
  freelancer = UserSerializer1(read_only=True)
  milestones = MilestoneSerializer1(many=True, read_only=True)
  participants = ContrParticipantSerializer1(many=True, read_only=True)
  terms = ContractTermSerializer1(many=True, read_only=True)
  contr_statuses = ContractStatusSerializer1(many=True, read_only=True)
  class Meta:
    model = Contract
    fields = ['client', 'freelancer', 'milestones', 'participants', 'terms', 'contr_statuses', 'title', 'description', 'total_amount', 'status', 'created_at']
    
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