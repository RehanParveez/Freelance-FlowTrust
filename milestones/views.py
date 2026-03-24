from django.shortcuts import render
from rest_framework import viewsets
from milestones.serializers.detail import MilestoneSerializer
from milestones.models import Milestone
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from payments.models import Payment, Escrow, Transaction
from django.db import transaction

# Create your views here.
class MilestoneViewset(viewsets.ModelViewSet):
  serializer_class = MilestoneSerializer
  queryset = Milestone.objects.all().order_by('id')
  permission_classes = [IsAuthenticated]
  
  def get_queryset(self):
    user = self.request.user
    if user.is_superuser:
      return Milestone.objects.all()
    client_miles = Milestone.objects.filter(contract__client=user)
    freelan_miles = Milestone.objects.filter(contract__freelancer=user)
    return client_miles | freelan_miles
  
  @action(detail=True, methods=['post'])
  def sub_milest(self, request, pk=None):
    milest = self.get_object()
    if request.user != milest.contract.freelancer:
      return Response({'err': 'freel can submit'}, status=403)
    if milest.status != 'pending':
      return Response({'err': 'milest cant be sub'}, status=400)
    milest.status = 'submitted'
    milest.save()
    return Response({'status': 'milest is sub'}, status=200)
  
  @action(detail=True, methods=['post'])
  @transaction.atomic
  def approve_milest(self, request, pk=None):
    milest = self.get_object()
    if request.user != milest.contract.client:
      return Response({'err': 'client can approve'}, status=403)
    if milest.status != 'submitted':
      return Response({'err': 'sub milest to be approv'}, status=400)
  
    escrow = Escrow.objects.filter(milestone=milest)
    escrow = escrow.first()
    if not escrow:
      return Response({'err': 'there is no escrow'}, status=400)
    if not escrow.is_funded:
      return Response({'err': 'escrow isnt funded so pay wont be relea'})
    if escrow.is_released:
        return Response({'err': 'it is released before'}, status=400)
    
    if Payment.objects.filter(escrow=escrow).exists():
      return Response({'err': 'pay exists'}, status=400)
    freel_wallet = escrow.freelancer.wallet
    freel_wallet.balance += escrow.amount
    freel_wallet.save()
    escrow.is_released = True
    escrow.save()
    
    Payment.objects.create(escrow=escrow, client=escrow.client, freelancer=escrow.freelancer, amount=escrow.amount)
    Transaction.objects.create(wallet=freel_wallet, amount=escrow.amount, transaction = 'deposit', description = 'pay of milest release')
    milest.status = 'approved'
    milest.save()
    return Response({'status': 'milest is appro & pay is relea'}, status=200)

  @action(detail=True, methods=['post'])
  def reject_miles(self, request, pk=None):
    milest = self.get_object()
    if request.user != milest.contract.client:
      return Response({'err': 'client can reject'}, status=403)
    if milest.status != 'submitted':
      return Response({'err': 'submitt milest can be rej'}, status=400)
    milest.status = 'rejected'
    milest.save()
    return Response({'status': 'miles is rej'}, status=200)


