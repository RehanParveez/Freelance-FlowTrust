from rest_framework import viewsets
from disputes.serializers.detail import DisputeSerializer, DisputeMessageSerializer, ProofSerializer, SolutionSerializer
from disputes.models import Dispute, DisputeMessage, Proof, Solution
from core.permissions import OwnerOrAdminPermission, AdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from payments.models import Escrow
from decimal import Decimal
from disputes.disputes.cache_utils import cache_dispute, get_dispute
from accounts.accounts.cache_utils import cache_dashboard

# Create your views here.
class DisputeViewset(viewsets.ModelViewSet):
  serializer_class = DisputeSerializer
  queryset = Dispute.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['description']
  ordering_fields = ['created_at']
  filterset_fields = ['description', 'status', 'created_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_disp = self.queryset.filter(contract__client=user)
    freel_disp = self.queryset.filter(contract__freelancer=user)
    return client_disp | freel_disp
  
  @action(detail=True, methods=['post'])
  def submit_proof(self, request, pk=None):
    dispute = self.get_object()
    user = request.user
    if user != dispute.contract.client:
      if user != dispute.contract.freelancer:
        return Response({'err': 'is not allowed'}, status=403)
    content = request.data.get('content')
    file = request.data.get('file')
    
    if not content:
      if not file:
        return Response({'err': 'provide the content & file'}, status=400)
    if content:
      DisputeMessage.objects.create(dispute=dispute, by=user, content=content)
    if file:
      Proof.objects.create(dispute=dispute, file=file)
    
    dispute.status = 'checking'
    dispute.save()
    cache_dispute(dispute.id)
    cache_dashboard(dispute.contract.client.id)
    cache_dashboard(dispute.contract.freelancer.id)
    return Response({'msg': 'the proof is submitted'}, status=200)
  
  @action(detail=True, methods=['post'])
  def solve_dispute(self, request, pk=None):
    dispute = self.get_object()
    user = request.user
    if user.control != 'admin':
      return Response({'err': 'the admin is allowed'}, status=403)
    if dispute.status == 'solved':
      return Response({'err': 'its solved already'}, status=400)
    if not dispute.milestone:
      return Response({'err': 'there is no milestone'}, status=400)

    escrow = Escrow.objects.filter(milestone=dispute.milestone)
    escrow = escrow.first()
    if not escrow:
      return Response({'err': 'the escrow is not found'}, status=400)
    
    if not escrow.is_funded:
      return Response({'err': 'the escrow is not funded'}, status=400)

    amount_to_freel = request.data.get('amount_rel_to_freel')
    amount_to_client = request.data.get('amount_ref_to_client')
    if not amount_to_freel:
      if not amount_to_client:
        return Response({'err': 'provide the amounts'}, status=400)
      
    amount_to_freel = Decimal(amount_to_freel or 0)
    amount_to_client = Decimal(amount_to_client or 0)
    amount = escrow.amount

    if amount_to_freel + amount_to_client != (amount):
      return Response({'err': 'the amounts are wrong'}, status=400)

    client_wallet = dispute.contract.client.wallet
    freel_wallet = dispute.contract.freelancer.wallet
    freel_wallet.balance += amount_to_freel
    client_wallet.balance += amount_to_client
    freel_wallet.save()
    client_wallet.save()

    escrow.is_released = True
    escrow.save()

    Solution.objects.create(dispute=dispute, solved_by=user, amount_rel_to_freel=amount_to_freel, amount_ref_to_client=amount_to_client)
    dispute.status = 'solved'
    dispute.save()
    cache_dispute(dispute.id)
    cache_dashboard(dispute.contract.client.id)
    cache_dashboard(dispute.contract.freelancer.id)
    
    return Response({'msg': 'the dispute is solved'}, status=200)
  
  @action(detail=True, methods=['post'])
  def close_dispute(self, request, pk=None):
    dispute = self.get_object()
    user = request.user
    if user != dispute.contract.client:
      if user != dispute.contract.freelancer:
        return Response({'err': 'cant close this dispute'}, status=403)
      
    if dispute.status != 'solved':
      return Response({'err': 'before closing the dispute should be solved'}, status=400)
    dispute.status = 'closed'
    dispute.save()
    cache_dispute(dispute.id)
    cache_dashboard(dispute.contract.client.id)
    cache_dashboard(dispute.contract.freelancer.id)
    
    return Response({'msg': 'the dispute is closed'}, status=200)
  
  @action(detail=True, methods=['get'])
  def stats(self, request, pk=None):
    data = get_dispute(pk)
    return Response(data)
  
class DisputeMessageViewset(viewsets.ModelViewSet):
  serializer_class = DisputeMessageSerializer
  queryset = DisputeMessage.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  
  # filtering fields
  search_fields = ['content']
  ordering_fields = ['created_at']
  filterset_fields = ['content', 'created_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_dismsg = self.queryset.filter(dispute__conract__client=user)
    freel_dismsg = self.queryset.filter(dispute__contract__freelancer=user)
    return client_dismsg | freel_dismsg
    
class ProofViewset(viewsets.ModelViewSet):
  serializer_class = ProofSerializer
  queryset = Proof.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['description']
  ordering_fields = ['uploaded_at']
  filterset_fields = ['description', 'uploaded_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_proof = self.queryset.filter(dispute__contract__client=user)
    freel_proof = self.queryset.filter(dispute__contract__freelancer=user)
    return client_proof | freel_proof
    
class SolutionViewset(viewsets.ModelViewSet):
  serializer_class = SolutionSerializer
  queryset = Solution.objects.all().order_by('id')
  permission_classes = [AdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['decision']
  ordering_fields = ['solved_at']
  filterset_fields = ['decision', 'solved_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_sol = self.queryset.filter(dispute__contract__client=user)
    freel_sol = self.queryset.filter(dispute__contract__freelancer=user)
    return client_sol | freel_sol



