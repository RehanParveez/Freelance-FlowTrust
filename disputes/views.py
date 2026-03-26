from django.shortcuts import render
from rest_framework import viewsets
from disputes.serializers.detail import DisputeSerializer, DisputeMessageSerializer, ProofSerializer, SolutionSerializer
from disputes.models import Dispute, DisputeMessage, Proof, Solution
from core.permissions import DisputePermission, DisputeMessagePermission, ProofPermission, SolutionPermission

# Create your views here.
class DisputeViewset(viewsets.ModelViewSet):
  serializer_class = DisputeSerializer
  queryset = Dispute.objects.all().order_by('id')
  permission_classes = [DisputePermission]

class DisputeMessageViewset(viewsets.ModelViewSet):
  serializer_class = DisputeMessageSerializer
  queryset = DisputeMessage.objects.all().order_by('id')
  permission_classes = [DisputeMessagePermission]
    
class ProofViewset(viewsets.ModelViewSet):
  serializer_class = ProofSerializer
  queryset = Proof.objects.all().order_by('id')
  permission_classes = [ProofPermission]
    
class SolutionViewset(viewsets.ModelViewSet):
  serializer_class = SolutionSerializer
  queryset = Solution.objects.all().order_by('id')
  permission_classes = [SolutionPermission]


