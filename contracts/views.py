from django.shortcuts import render
from rest_framework import viewsets
from contracts.serializers.detail import ContractSerializer, ContrParticipantSerializer, ContractTermSerializer, ContractStatusSerializer
from contracts.models import Contract, ContrParticipant, ContractTerm, ContractStatus
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from milestones.serializers.detail import MilestoneSerializer
from rest_framework.response import Response
from core.permissions import ContractPermission

# Create your views here.
class ContractViewset(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all().order_by('id')
    permission_classes = [IsAuthenticated, ContractPermission]
    
    def get_queryset(self):
      user = self.request.user
      if user.control == 'admin':
        return self.queryset
      client_contr = self.queryset.filter(client=user)
      freelan_contr = self.queryset.filter(freelancer=user)
      return client_contr | freelan_contr
    
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

class ContrParticipantViewset(viewsets.ModelViewSet):
  serializer_class = ContrParticipantSerializer
  queryset = ContrParticipant.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, ContractPermission]
  
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
  permission_classes = [IsAuthenticated, ContractPermission]
  
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
  permission_classes = [IsAuthenticated, ContractPermission]
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
        return self.queryset
    client_contrstat = self.queryset.filter(contract__client=user)
    freelan_contrstat = self.queryset.filter(contract__freelancer=user)
    return client_contrstat | freelan_contrstat
  


    
    
