from rest_framework import serializers
from accounts.serializers.basic import UserSerializer1
from marketplace.serializers.basic import SkillSerializer1, PortfolioSerializer1, ProposalSerializer1, FreelancerProfileSerializer1
from marketplace.models import Skill, FreelancerProfile, Portfolio, JobPost, Proposal

class SkillSerializer(serializers.ModelSerializer):
  class Meta:
    model = Skill
    fields = ['name', 'category', 'created_at']
    
class FreelancerProfileSerializer(serializers.ModelSerializer):
  user = UserSerializer1(read_only=True)
  skill = SkillSerializer1(many=True, read_only=True)
  portfolios = PortfolioSerializer1(many=True, read_only=True)
  class Meta:
    model = FreelancerProfile
    fields = ['user', 'skill', 'portfolios', 'bio', 'hour_rate', 'portf_url']
    
class PortfolioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Portfolio
    fields = ['freelancer', 'title', 'description', 'link', 'created_at']
    
class JobPostSerializer(serializers.ModelSerializer):
  client = UserSerializer1(read_only=True)
  proposals = ProposalSerializer1(many=True, read_only=True)
  class Meta:
    model = JobPost
    fields = ['client', 'proposals', 'name', 'description', 'budget', 'is_active', 'created_at']
    
class ProposalSerializer(serializers.ModelSerializer):
  freelancer = FreelancerProfileSerializer1(read_only=True)
  class Meta:
    model = Proposal
    fields = ['job', 'freelancer', 'proposed_amount', 'submitted_at', 'is_accepted']