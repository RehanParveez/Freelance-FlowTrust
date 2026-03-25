from django.shortcuts import render
from rest_framework import viewsets
from marketplace.serializers.detail import SkillSerializer, FreelancerProfileSerializer, PortfolioSerializer, JobPostSerializer, ProposalSerializer 
from marketplace.models import Skill, FreelancerProfile, Portfolio, JobPost, Proposal
from rest_framework.permissions import IsAuthenticated
from core.permissions import OwnerPermission, ClientPermission, JobPermission, ProposalPermission

# Create your views here.
class SkillViewset(viewsets.ModelViewSet):
  serializer_class = SkillSerializer
  queryset = Skill.objects.all().order_by('id')
  permission_classes = [IsAuthenticated]
    
  def get_queryset(self):
    return self.queryset
    
class FreelancerProfileViewset(viewsets.ModelViewSet):
  serializer_class = FreelancerProfileSerializer
  queryset = FreelancerProfile.objects.all().order_by('id')
  permission_classes = [IsAuthenticated]
  
  def get_queryset(self):
    return self.queryset
  
class PortfolioViewset(viewsets.ModelViewSet):
  serializer_class = PortfolioSerializer
  queryset = Portfolio.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, OwnerPermission]
  
  def get_queryset(self):
    return self.queryset.filter(freelancer__user=self.request.user)
    
class JobPostViewset(viewsets.ModelViewSet):
  serializer_class = JobPostSerializer
  queryset = JobPost.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, ClientPermission, JobPermission]
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'client':
        return self.queryset.filter(client=user)
    return self.queryset
    
class ProposalViewset(viewsets.ModelViewSet):
  serializer_class = ProposalSerializer
  queryset = Proposal.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, ProposalPermission]
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'client':
      return self.queryset.filter(client=user)
    return self.queryset

    