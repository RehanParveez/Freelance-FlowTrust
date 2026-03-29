from contracts.models import Contract
from django.core.cache import cache

def cache_contr_stats(contract_id):
  contr = Contract.objects.get(id=contract_id)
  total = contr.milestones.count()
  approved = contr.milestones.filter(is_approved=True)
  approved = approved.count()
  pending = contr.milestones.filter(is_approved=False)
  pending = pending.count()
    
  data = {'total_milestones': total, 'approved': approved, 'pending': pending, 'status': contr.status}
  cache.set(f'contract:{contract_id}', data)
  print(f'the contract {contract_id}: {data}')

def get_contr_stats(contract_id):
  data = cache.get(f'contract:{contract_id}')
    
  if data is None:
    print(f' the contract {contract_id}')
    cache_contr_stats(contract_id)
    data = cache.get(f'contract:{contract_id}')
  else:
    print(f'the contract is {contract_id}')
    
  return data