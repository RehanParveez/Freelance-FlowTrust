from django.shortcuts import render
from rest_framework import viewsets
from disputes.serializers.detail import DisputeSerializer, DisputeMessageSerializer, ProofSerializer, SolutionSerializer
from disputes.models import Dispute, DisputeMessage, Proof, Solution
from core.permissions import DisputePermission, DisputeMessagePermission, ProofPermission, SolutionPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class DisputeViewset(viewsets.ModelViewSet):
  serializer_class = DisputeSerializer
  queryset = Dispute.objects.all().order_by('id')
  permission_classes = [DisputePermission]
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

class DisputeMessageViewset(viewsets.ModelViewSet):
  serializer_class = DisputeMessageSerializer
  queryset = DisputeMessage.objects.all().order_by('id')
  permission_classes = [DisputeMessagePermission]
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
  permission_classes = [ProofPermission]
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
  permission_classes = [SolutionPermission]
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



