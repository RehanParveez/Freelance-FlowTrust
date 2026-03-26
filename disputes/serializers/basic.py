from rest_framework import serializers
from disputes.models import Dispute, DisputeMessage, Proof, Solution

class DisputeSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Dispute
    fields = ['contract', 'raised_by', 'reason', 'status']
        
class DisputeMessageSerializer1(serializers.ModelSerializer):
  class Meta:
    model = DisputeMessage
    fields = ['dispute', 'sender']

class ProofSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Proof
    fields = ['dispute', 'uploaded_by', 'file']

class SolutionSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Solution
    fields = ['dispute', 'admin', 'decision']