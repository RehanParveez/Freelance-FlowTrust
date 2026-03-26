from django.shortcuts import render
from rest_framework import viewsets
from analytics.serializers import UserAnalyticsSerializer, EarningReportSerializer, ContractAnalyticsSerializer
from analytics.models import UserAnalytics, EarningReport, ContractAnalytics
from core.permissions import AnalyticsPermission

# Create your views here.
class UserAnalyticsViewset(viewsets.ModelViewSet):
  serializer_class = UserAnalyticsSerializer
  queryset = UserAnalytics.objects.all().order_by('id')
  permission_classes = [AnalyticsPermission]

class EarningReportViewset(viewsets.ModelViewSet):
  serializer_class = EarningReportSerializer
  queryset = EarningReport.objects.all().order_by('id')
  permission_classes = [AnalyticsPermission]
    
class ContractAnalyticsViewset(viewsets.ModelViewSet):
  serializer_class = ContractAnalyticsSerializer
  queryset = ContractAnalytics.objects.all().order_by('id')
  permission_classes = [AnalyticsPermission]
    



