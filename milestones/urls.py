from django.urls import path, include
from milestones.views import MilestoneViewset, MilestoneSubmissionViewset, MilestoneReviewViewset, MilestoneStatusViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'milestone', MilestoneViewset, basename = 'milestone')
router.register(r'milestonesubmission', MilestoneSubmissionViewset, basename = 'milestonesubmission')
router.register(r'milestonereview', MilestoneReviewViewset, basename = 'milestonereview')
router.register(r'milestonestatus', MilestoneStatusViewset, basename = 'milestonestatus')

urlpatterns = [
  path('', include(router.urls)),
]