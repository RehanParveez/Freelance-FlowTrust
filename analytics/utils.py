from analytics.models import UserAnalytics, EarningReport, ContractAnalytics

def user_analytics(user, field, amount=1):
  analytics, _ = UserAnalytics.objects.get_or_create(user=user)
  if field == 'total_contr':
    analytics.total_contr += 1
  elif field == 'completed_contr':
    analytics.completed_contr += 1
  elif field == 'total_earnings':
    analytics.total_earnings += amount
    
  analytics.save()

def earning_report(user, contract, amount):
  EarningReport.objects.create(user=user, contract=contract, amount=amount)

def contract_analytics(contract, field, amount=1):
  analytics, _ = ContractAnalytics.objects.get_or_create(contract=contract)
  if field == 'total_milest':
    analytics.total_milest += 1
  elif field == 'milest_completed':
    analytics.milest_completed += 1
  elif field == 'total_pay':
    analytics.total_pay += amount
    
  analytics.save()
    