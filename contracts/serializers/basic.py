from rest_framework import serializers
from contracts.models import Contract, ContrParticipant, ContractTerm, ContractStatus, Activity

class ContractSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Contract
    fields = ['client', 'freelancer', 'title', 'description']
    
class ContrParticipantSerializer1(serializers.ModelSerializer):
  class Meta:
    model = ContrParticipant
    fields = ['contract', 'user']
    
class ContractTermSerializer1(serializers.ModelSerializer):
  class Meta:
    model = ContractTerm
    fields = ['contract', 'description']
    
class ContractStatusSerializer1(serializers.ModelSerializer):
  class Meta:
    model = ContractStatus
    fields = ['contract', 'prev_status', 'new_status']

class ActivitySerializer1(serializers.ModelSerializer):
  class Meta:
    model = Activity
    fields = ['user', 'action_type', 'content_type']