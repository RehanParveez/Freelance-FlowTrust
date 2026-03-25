from django.shortcuts import render
from rest_framework import viewsets
from payments.serializers.detail import WalletSerializer, PaymentSerializer, PaymentMethodSerializer
from payments.models import Wallet, Payment, Escrow, Transaction, Refund, PaymentMethod
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from milestones.models import Milestone
from rest_framework.response import Response
from decimal import Decimal
from core.permissions import OwnerPermission, PaymentPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class WalletViewset(viewsets.ModelViewSet):
  serializer_class = WalletSerializer
  queryset = Wallet.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, OwnerPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['balance']
  ordering_fields = ['balance']
  filterset_fields = ['balance']
    
  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)
    
class PaymentViewset(viewsets.ModelViewSet):
  serializer_class = PaymentSerializer
  queryset = Payment.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, PaymentPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['amount']
  ordering_fields = ['created_at']
  filterset_fields = ['amount', 'created_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_pay = self.queryset.filter(client=user)
    freelan_pay = self.queryset.filter(freelancer=user)
    return client_pay | freelan_pay
    
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
    if milest.status == 'approved':
      return Response({'err': 'the approved milest cant be refund'}, status=400)
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
  
class PaymentMethodViewset(viewsets.ModelViewSet):
  serializer_class = PaymentMethodSerializer
  queryset = PaymentMethod.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, OwnerPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['method_type']
  ordering_fields = ['method_type']
  filterset_fields = ['is_default', 'method_type']
  
  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)
    
    
