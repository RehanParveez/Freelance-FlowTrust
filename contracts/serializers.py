from rest_framework import serializers
from contracts.models import Contract

class ContractSerializer(serializers.ModelSerializer):
  class Meta:
    model = Contract
    fields = ['client', 'freelancer', 'title', 'description', 'total_amount', 'status', 'created_at']