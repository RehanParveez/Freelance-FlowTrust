from django.contrib import admin
from marketplace.models import Skill, FreelancerProfile, Portfolio, JobPost, Proposal

# Register your models here.
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_at']
    
@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'hour_rate', 'portf_url']

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['freelancer', 'title', 'description', 'link', 'created_at']

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ['client', 'name', 'description', 'budget', 'is_active', 'created_at']
    
@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['job', 'freelancer', 'proposed_amount', 'submitted_at', 'is_accepted']
