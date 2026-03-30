from rest_framework import viewsets
from analytics.serializers import UserAnalyticsSerializer, EarningReportSerializer, ContractAnalyticsSerializer
from analytics.models import UserAnalytics, EarningReport, ContractAnalytics
from core.permissions import AdminPermission, OwnerOrAdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg
from rest_framework.response import Response
from django.db.models.functions import TruncMonth

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

class UserAnalyticsView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    user = request.user
    analytics = getattr(user, 'analytics', None)
    earnings = EarningReport.objects.filter(user=user).aggregate(total_earnings=Sum('amount'), average_earning=Avg('amount'))

    total_contracts = 0
    completed_contracts = 0
    if analytics:
      total_contracts = analytics.total_contr
      completed_contracts = analytics.completed_contr

    total_earnings = earnings.get('total_earnings')
    if total_earnings is None:
      total_earnings = 0

    average_earning = earnings.get('average_earning')
    if average_earning is None:
      average_earning = 0
    res = {'total_contracts': total_contracts, 'completed_contracts': completed_contracts, 'total_earnings': total_earnings, 'average_earning': average_earning}
    return Response(res)

class ContractAnalyticsView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request, contract_id):
    analy = ContractAnalytics.objects.filter(contract_id=contract_id)
    analy = analy.first()

    if not analy:
      return Response({'err': 'there is no analy for this contr'}, status=404)
    contract = analy.contract
    user = request.user
    if user != contract.client and user != contract.freelancer:
      return Response({'err': 'its not allowed'}, status=403)
    res = {'total_milestones': analy.total_milest, 'milestones_completed': analy.milest_completed, 'total_pay': analy.total_pay}
    return Response(res)

class EarningsView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    user = request.user
    queryset = (EarningReport.objects.filter(user=user).annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('amount')).order_by('month'))
    res = []
    for val in queryset:
      res.append({'month': val['month'].strftime("%Y-%m"), 'total': val['total']})
    return Response(res)

class DashboardView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    user = request.user
    analytics = getattr(user, 'analytics', None)
    total_contracts = 0
    completed_contracts = 0

    if analytics:
      total_contracts = analytics.total_contr
      completed_contracts = analytics.completed_contr

    earnings = EarningReport.objects.filter(user=user).aggregate(total=Sum('amount'))
    total_earn = earnings.get('total')
    if total_earn is None:
      total_earn = 0

    client_data = ContractAnalytics.objects.filter(contract__client=user).aggregate(total=Sum('milest_completed'))
    freel_data = ContractAnalytics.objects.filter(contract__freelancer=user).aggregate(total=Sum('milest_completed'))
    client_tot = client_data.get('total')
    if client_tot is None:
      client_tot = 0
    freel_total = freel_data.get('total')
    if freel_total is None:
      freel_total = 0

    milest_completed = client_tot + freel_total
    user_data = {'total_contracts': total_contracts, 'completed_contracts': completed_contracts, 'total_earnings': total_earn}
    res = {'user_data': user_data, 'milest_completed': milest_completed}
    return Response(res)
    