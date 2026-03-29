from django.core.cache import cache
from payments.models import Wallet
from contracts.models import Contract
from milestones.models import Milestone
from disputes.models import Dispute

def cache_dashboard(user_id):
  wallet = Wallet.objects.get(user_id=user_id)
  client_contr = Contract.objects.filter(status = 'active', client_id=user_id)
  client_contr = client_contr.count()
  freelancer_contr = Contract.objects.filter(status = 'active', freelancer_id=user_id)
  freelancer_contr = freelancer_contr.count()
  active_contr = client_contr + freelancer_contr

  client_milest = Milestone.objects.filter(status = 'pending', contract__client_id=user_id)
  client_milest = client_milest.count()
  freelancer_milest = Milestone.objects.filter(status = 'pending', contract__freelancer_id=user_id)
  freelancer_milest = freelancer_milest.count()
  pending_milest = client_milest + freelancer_milest

  client_disp = Dispute.objects.filter(status = 'open', contract__client_id=user_id)
  client_disp = client_disp.count()
  freelancer_disp = Dispute.objects.filter(status = 'open', contract__freelancer_id=user_id)
  freelancer_disp = freelancer_disp.count()
  open_disp = client_disp + freelancer_disp

  data = {'wallet': str(wallet.balance), 'active_contracts': active_contr, 'pending_milestones': pending_milest,
    'open_disputes': open_disp}

  cache.set(f'dashboard:{user_id}', data, timeout=220)
  print(f'the dashboard {user_id}: {data}')
  
def get_dashboard(user_id):
  data = cache.get(f'dashboard:{user_id}')
    
  if data is None:
    print(f'the dashboard {user_id}')
    cache_dashboard(user_id)
    
    data = cache.get(f'dashboard:{user_id}')
  else:
    print(f'the dashboard {user_id}')
    
  return data
  
    
