from disputes.models import Dispute
from django.core.cache import cache

def cache_dispute(dispute_id):
  dispute = Dispute.objects.get(id=dispute_id)
  milestone_id = None
  if dispute.milestone:
    milestone_id = dispute.milestone.id

  data = {'id': dispute.id, 'status': dispute.status, 'contract_id': dispute.contract.id, 'milestone_id': milestone_id,
    'raised_by': dispute.raised_by.id, 'description': dispute.description}
  cache.set(f'dispute:{dispute_id}', data)
  print(f'the dispute {dispute_id}: {data}')

def get_dispute(dispute_id):
  data = cache.get(f'dispute:{dispute_id}')
  if data is None:
    print(f'the dispute {dispute_id}')
    cache_dispute(dispute_id)
    data = cache.get(f'dispute:{dispute_id}')
  else:
    print(f'the dispute {dispute_id}')
    
  return data