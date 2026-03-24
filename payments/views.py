from django.shortcuts import render
from rest_framework import viewsets
from payments.serializers.detail import PaymentSerializer
from payments.models import Payment, Escrow, Transaction, Refund
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from milestones.models import Milestone
from rest_framework.response import Response
from decimal import Decimal

# Create your views here.
class PaymentViewset(viewsets.ModelViewSet):
  serializer_class = PaymentSerializer
  queryset = Payment.objects.all().order_by('id')
  permission_classes = [IsAuthenticated]
  
  @action(detail=True, methods=['post'])
  @transaction.atomic()
  def deposit(self, request, pk=None):
    milest = Milestone.objects.get(id=pk)
    if request.user != milest.contract.client:
      return Response({'err': 'clinet can deposit'}, status=403)
    amount = Decimal(request.data.get('amount', 0))
    
    if amount <= 0:
      return Response({'err': 'inv amount'}, status=400)
    wallet = request.user.wallet
    if wallet.balance < amount:
      return Response({'err': 'balance is less'}, status=400)
    wallet.balance -= amount
    wallet.save()
    
    escrow, created = Escrow.objects.get_or_create(milestone=milest, defaults={
      'client': milest.contract.client, 'freelancer': milest.contract.freelancer, 'amount': amount, 'is_funded': True})
    
    if not created:
      escrow.amount += amount
      escrow.is_funded = True
      escrow.save()
    Transaction.objects.create(wallet=wallet, amount=amount, transaction = 'withdraw', description = 'deposit to escrow')
    return Response({'status': 'the deposit is done'}, status=200)
   
  @action(detail=False, methods=['get'])
  def wallet(self, request):
     wallet = request.user.wallet
     return Response({'balance': wallet.balance})
  
  @action(detail=True, methods=['post'])
  @transaction.atomic
  def refund(self, request, pk=None):
    payment = Payment.objects.get(id=pk)
    escrow = payment.escrow
    milest = escrow.milestone
    if request.user != milest.contract.client:
      return Response({'err': 'client can refund'}, status=403)
    if escrow.is_released:
      return Response({'err': 'is already released'}, status=400)
    wallet = escrow.client.wallet
    wallet.balance += escrow.amount
    wallet.save()
    
    Refund.objects.create(payment=payment, amount=escrow.amount, reason = 'refunding before the approval')
    Transaction.objects.create(wallet=wallet, amount=escrow.amount, transaction = 'refund', description = 'refunding from the escrow')
    escrow.delete()
    return Response({'status': 'the refund is done'}, status=200)
