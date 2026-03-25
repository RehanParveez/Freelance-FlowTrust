from django.urls import path, include
from marketplace.views import SkillViewset, FreelancerProfileViewset, PortfolioViewset, JobPostViewset, ProposalViewset 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'skill', SkillViewset, basename = 'skill')
router.register(r'freelancerprofile', FreelancerProfileViewset, basename = 'freelancerprofile')
router.register(r'portfolio', PortfolioViewset, basename = 'portfolio')
router.register(r'jobpost', JobPostViewset, basename = 'jobpost')
router.register(r'proposal', ProposalViewset, basename = 'proposal')

urlpatterns = [
  path('', include(router.urls)),
]