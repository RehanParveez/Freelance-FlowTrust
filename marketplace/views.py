from django.shortcuts import render
from rest_framework import viewsets
from marketplace.serializers.detail import SkillSerializer, FreelancerProfileSerializer, PortfolioSerializer, JobPostSerializer, ProposalSerializer 
from marketplace.models import Skill, FreelancerProfile, Portfolio, JobPost, Proposal
from rest_framework.permissions import IsAuthenticated
from core.permissions import OwnerPermission, ClientPermission, JobPermission, ProposalPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class SkillViewset(viewsets.ModelViewSet):
  serializer_class = SkillSerializer
  queryset = Skill.objects.all().order_by('id')
  permission_classes = [IsAuthenticated]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['name']
  ordering_fields = ['created_at']
  filterset_fields = ['category', 'created_at']
    
  def get_queryset(self):
    return self.queryset
    
class FreelancerProfileViewset(viewsets.ModelViewSet):
  serializer_class = FreelancerProfileSerializer
  queryset = FreelancerProfile.objects.all().order_by('id')
  permission_classes = [IsAuthenticated]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['bio']
  ordering_fields = ['hour_rate']
  filterset_fields = ['bio', 'hour_rate']
  
  def get_queryset(self):
    return self.queryset
  
class PortfolioViewset(viewsets.ModelViewSet):
  serializer_class = PortfolioSerializer
  queryset = Portfolio.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, OwnerPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['title']
  ordering_fields = ['created_at']
  filterset_fields = ['title', 'description', 'created_at']
  
  def get_queryset(self):
    return self.queryset.filter(freelancer__user=self.request.user)
    
class JobPostViewset(viewsets.ModelViewSet):
  serializer_class = JobPostSerializer
  queryset = JobPost.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, ClientPermission, JobPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['name']
  ordering_fields = ['created_at']
  filterset_fields = ['name', 'description', 'created_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'client':
        return self.queryset.filter(client=user)
    return self.queryset
    
class ProposalViewset(viewsets.ModelViewSet):
  serializer_class = ProposalSerializer
  queryset = Proposal.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, ProposalPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['proposed_amount']
  ordering_fields = ['submitted_at']
  filterset_fields = ['proposed_amount', 'submitted_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'client':
      return self.queryset.filter(client=user)
    return self.queryset

    