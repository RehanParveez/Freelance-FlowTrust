from rest_framework import viewsets
from milestones.serializers.detail import MilestoneSerializer, MilestoneSubmissionSerializer, MilestoneReviewSerializer, MilestoneStatusSerializer
from milestones.models import Milestone, MilestoneSubmission, MilestoneReview, MilestoneStatus
from rest_framework.decorators import action
from rest_framework.response import Response
from payments.models import Payment, Escrow, Transaction
from django.db import transaction
from core.permissions import OwnerOrAdminPermission, FreelancerPermission, ClientPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class MilestoneViewset(viewsets.ModelViewSet):
  serializer_class = MilestoneSerializer
  queryset = Milestone.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['title']
  ordering_fields = ['is_submitted']
  filterset_fields = ['title', 'order', 'status', 'is_submitted']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_milest = self.queryset.filter(contract__client=user)
    freelan_milest = self.queryset.filter(contract__freelancer=user)
    return client_milest | freelan_milest
  
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
    
    prev = Milestone.objects.filter(contract=milest.contract, order__lt=milest.order)
    if prev.exclude(status='approved').exists():
        return Response({'err': 'prev milests should be comp first'}, status=400)
  
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
  
class MilestoneSubmissionViewset(viewsets.ModelViewSet):
  serializer_class = MilestoneSubmissionSerializer
  queryset = MilestoneSubmission.objects.all().order_by('id')
  permission_classes = [FreelancerPermission, OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['notes']
  ordering_fields = ['submitted_at']
  filterset_fields = ['notes', 'submitted_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_milestsub = self.queryset.filter(milestone__contract__client=user)
    freelan_milestsub = self.queryset.filter(milestone__contract__freelancer=user)
    return client_milestsub | freelan_milestsub
    
class MilestoneReviewViewset(viewsets.ModelViewSet):
  serializer_class = MilestoneReviewSerializer
  queryset = MilestoneReview.objects.all().order_by('id')
  permission_classes = [ClientPermission, OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['email']
  ordering_fields = ['reviewed_at']
  filterset_fields = ['rating', 'reviewed_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_milestrev = self.queryset.filter(submission__milestone__contract__client=user)
    freelan_milestrev = self.queryset.filter(submission__milestone__contract__freelancer=user)
    return client_milestrev | freelan_milestrev
  
class MilestoneStatusViewset(viewsets.ModelViewSet):
  serializer_class = MilestoneStatusSerializer
  queryset = MilestoneStatus.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['prev_status']
  ordering_fields = ['new_status']
  filterset_fields = ['date', 'new_status']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_mileststat = self.queryset.filter(milestone__contract__client=user)
    freelan_mileststat = self.queryset.filter(milestone__contract__freelancer=user)
    return client_mileststat | freelan_mileststat
    
    