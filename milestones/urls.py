from django.urls import path, include
from milestones.views import MilestoneViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'milestone', MilestoneViewset, basename = 'milestone')

urlpatterns = [
  path('', include(router.urls)),
]