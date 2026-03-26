from rest_framework import serializers
from disputes.serializers.basic import DisputeMessageSerializer1, ProofSerializer1, SolutionSerializer1
from contracts.serializers.basic import ContractSerializer1
from milestones.serializers.basic import MilestoneSerializer1
from disputes.models import Dispute, DisputeMessage, Proof, Solution

class DisputeSerializer(serializers.ModelSerializer):
  messages = DisputeMessageSerializer1(many=True, read_only=True)
  proofs = ProofSerializer1(many=True, read_only=True)
  solutions = SolutionSerializer1(read_only=True)
  contract = ContractSerializer1(read_only=True)
  milestone = MilestoneSerializer1(read_only=True)
  class Meta:
    model = Dispute
    fields = ['contract', 'milestone', 'raised_by', 'reason', 'proofs', 'status', 'created_at', 'messages', 'solutions']
        
class DisputeMessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = DisputeMessage
    fields = ['dispute', 'sender', 'message', 'created_at']

class ProofSerializer(serializers.ModelSerializer):
  class Meta:
    model = Proof
    fields = ['dispute', 'uploaded_by', 'file', 'description', 'uploaded_at']

class SolutionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Solution
    fields = ['dispute', 'admin', 'decision', 'notes', 'resolved_at']

