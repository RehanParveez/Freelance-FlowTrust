from django.shortcuts import render
from rest_framework import viewsets
from contracts.serializers import ContractSerializer
from contracts.models import Contract
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from milestones.serializers import MilestoneSerializer
from rest_framework.response import Response

# Create your views here.
class ContractViewset(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
      user = self.request.user
      if user.is_superuser:
        return Contract.objects.all()
      client_contr = Contract.objects.filter(client=user)
      freelan_contr = Contract.objects.filter(freelancer=user)
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
  


    
    
