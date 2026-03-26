from django.contrib import admin
from analytics.models import UserAnalytics, EarningReport, ContractAnalytics

# Register your models here.
@admin.register(UserAnalytics)
class UserAnalyticsAdmin(admin.ModelAdmin):
  list_display = ['user', 'total_contr', 'completed_contr', 'total_earnings']

@admin.register(EarningReport)
class EarningReportAdmin(admin.ModelAdmin):
  list_display = ['user', 'contract', 'amount', 'created_at'] 

@admin.register(ContractAnalytics)
class ContractAnalyticsAdmin(admin.ModelAdmin):
  list_display = ['contract', 'total_milest', 'milest_completed', 'total_pay']
  
