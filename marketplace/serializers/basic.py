from rest_framework import serializers
from marketplace.models import Skill, FreelancerProfile, Portfolio, JobPost, Proposal
 
class SkillSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Skill
    fields = ['name', 'category']
    
class FreelancerProfileSerializer1(serializers.ModelSerializer):
  class Meta:
    model = FreelancerProfile
    fields = ['user', 'skill', 'bio']
    
class PortfolioSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Portfolio
    fields = ['freelancer', 'title']
    
class JobPostSerializer1(serializers.ModelSerializer):
  class Meta:
    model = JobPost
    fields = ['client', 'name', 'description']
    
class ProposalSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Proposal
    fields = ['job', 'freelancer']