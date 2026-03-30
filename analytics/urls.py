from django.urls import path, include
from analytics.views import UserAnalyticsViewset, EarningReportViewset, ContractAnalyticsViewset, UserAnalyticsView, ContractAnalyticsView, EarningsView, DashboardView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'useranalytics', UserAnalyticsViewset, basename = 'useranalytics')
router.register(r'earningreport', EarningReportViewset, basename = 'earningreport')
router.register(r'contractanalytics', ContractAnalyticsViewset, basename = 'contractanalytics')

urlpatterns = [
  path('', include(router.urls)),
  path('useranaly/', UserAnalyticsView.as_view(), name = 'user_analy'),
  path('contractanaly/<int:contract_id>/', ContractAnalyticsView.as_view(), name = 'contractanaly'),
  path('earningsview/', EarningsView.as_view(), name = 'earnings_view'),
  path('dashboardview/', DashboardView.as_view(), name = 'dashboard_view'),
  
]

