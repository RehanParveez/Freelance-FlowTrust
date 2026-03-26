from rest_framework import serializers
from analytics.models import UserAnalytics, EarningReport, ContractAnalytics

class UserAnalyticsSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserAnalytics
    fields = ['user', 'total_contr', 'completed_contr', 'total_earnings']
      
class EarningReportSerializer(serializers.ModelSerializer):
  class Meta:
    model = EarningReport
    fields = ['user', 'contract', 'amount', 'created_at']

class ContractAnalyticsSerializer(serializers.ModelSerializer):
  class Meta:
    model = ContractAnalytics
    fields = ['contract', 'total_milest', 'milest_completed', 'total_pay']