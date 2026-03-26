from django.urls import path, include
from analytics.views import UserAnalyticsViewset, EarningReportViewset, ContractAnalyticsViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'useranalytics', UserAnalyticsViewset, basename = 'useranalytics')
router.register(r'earningreport', EarningReportViewset, basename = 'earningreport')
router.register(r'contractanalytics', ContractAnalyticsViewset, basename = 'contractanalytics')

urlpatterns = [
  path('', include(router.urls)),
]

