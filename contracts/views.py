from django.shortcuts import render
from rest_framework import viewsets
from contracts.serializers.detail import ContractSerializer, ContrParticipantSerializer, ContractTermSerializer, ContractStatusSerializer, ActivitySerializer
from contracts.models import Contract, ContrParticipant, ContractTerm, ContractStatus, Activity
from rest_framework.decorators import action
from milestones.serializers.detail import MilestoneSerializer
from rest_framework.response import Response
from core.permissions import ClientPermission, OwnerOrAdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class ContractViewset(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all().order_by('id')
    permission_classes = [ClientPermission, OwnerOrAdminPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
    search_fields = ['title']
    ordering_fields = ['created_at']
    filterset_fields = ['title', 'description', 'total_amount', 'created_at']
    
    def get_queryset(self):
      user = self.request.user
      if user.control == 'admin':
        return self.queryset
      client_contr = self.queryset.filter(client=user)
      freelan_contr = self.queryset.filter(freelancer=user)
      return client_contr | freelan_contr
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_milest(self, request, pk=None):
      contr = self.get_object()
      if request.user != contr.client:
        return Response({'err': 'client can add milest'}, status=403)
      serializer = MilestoneSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save(contract=contr)
        return Response(serializer.data, status=201)
      return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['post'])
    def accept_contr(self, request, pk=None):
      contr = self.get_object()

      if request.user != contr.freelancer:
        return Response({'err': 'freelancer can accept'}, status=403)
      if contr.status != 'pending':
        return Response({'err': 'its a wrong state'}, status=400)
      contr.status = 'active'
      contr.save()
      return Response({'status': 'contract is activated'}, status=200)
   
    @action(detail=True, methods=['post'])
    def complete_contr(self, request, pk=None):
      contr = self.get_object()
      if request.user != contr.client:
        return Response({'err': 'the contract can be comp by the client'}, status=403)
      if contr.status != 'active':
        return Response({'err': 'the contract is not active'}, status=400)
      
      for milest in contr.milestones.all():
        if not milest.is_approved:
          return Response({'error': 'All milestones must be approved'}, status=400)
      contr.status = 'completed'
      contr.save()
      return Response({'status': 'the contract is completed'}, status=200)

class ContrParticipantViewset(viewsets.ModelViewSet):
  serializer_class = ContrParticipantSerializer
  queryset = ContrParticipant.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['role']
  ordering_fields = ['role']
  filterset_fields = ['role']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
        return self.queryset
    client_contrpart = self.queryset.filter(contract__client=user)
    freelan_contrpart = self.queryset.filter(contract__freelancer=user)
    return client_contrpart | freelan_contrpart
    
class ContractTermViewset(viewsets.ModelViewSet):
  serializer_class = ContractTermSerializer
  queryset = ContractTerm.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['description']
  ordering_fields = ['created_at']
  filterset_fields = ['description', 'created_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
        return self.queryset
    client_contrterm = self.queryset.filter(contract__client=user)
    freelan_contrterm = self.queryset.filter(contract__freelancer=user)
    return client_contrterm | freelan_contrterm
    
class ContractStatusViewset(viewsets.ModelViewSet):
  serializer_class = ContractStatusSerializer
  queryset = ContractStatus.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['prev_status']
  ordering_fields = ['new_status']
  filterset_fields = ['prev_status', 'date']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
        return self.queryset
    client_contrstat = self.queryset.filter(contract__client=user)
    freelan_contrstat = self.queryset.filter(contract__freelancer=user)
    return client_contrstat | freelan_contrstat

class ActivityViewset(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all().order_by('id')
    permission_classes = [OwnerOrAdminPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
    search_fields = ['action_type']
    ordering_fields = ['action_type']
    filterset_fields = ['object_id', 'date']
    
    


    
    
