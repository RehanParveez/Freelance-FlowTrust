from rest_framework import viewsets
from analytics.serializers import UserAnalyticsSerializer, EarningReportSerializer, ContractAnalyticsSerializer
from analytics.models import UserAnalytics, EarningReport, ContractAnalytics
from core.permissions import AdminPermission, OwnerOrAdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class UserAnalyticsViewset(viewsets.ModelViewSet):
  serializer_class = UserAnalyticsSerializer
  queryset = UserAnalytics.objects.all().order_by('id')
  permission_classes = [AdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['total_contr']
  ordering_fields = ['completed_contr']
  filterset_fields = [ 'total_earnings', 'total_contr']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    return self.queryset.filter(user=user)

class EarningReportViewset(viewsets.ModelViewSet):
  serializer_class = EarningReportSerializer
  queryset = EarningReport.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['amount']
  ordering_fields = ['created_at']
  filterset_fields = ['amount',  'created_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    return self.queryset.filter(user=user)
    
class ContractAnalyticsViewset(viewsets.ModelViewSet):
  serializer_class = ContractAnalyticsSerializer
  queryset = ContractAnalytics.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['total_milest']
  ordering_fields = ['total_pay']
  filterset_fields = ['milest_completed', 'total_milest']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_anal = self.queryset.filter(contract__client=user)
    freel_anal = self.queryset.filter(contract__freelancer=user)
    return client_anal | freel_anal
    



