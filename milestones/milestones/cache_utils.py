from milestones.models import Milestone
from django.core.cache import cache

def cache_milest_stats(milestone_id):
  milestone = Milestone.objects.get(id=milestone_id)
  data = {'status': milestone.status, 'is_submitted': milestone.is_submitted, 'is_approved': milestone.is_approved, 'amount': str(milestone.amount)}
  cache.set(f'milestone:{milestone_id}', data)
  print(f'the milestone {milestone_id}: {data}')

def get_milest_stats(milestone_id):
  data = cache.get(f'milestone:{milestone_id}')
  if data is None:
    print(f'the milestone {milestone_id}')
    cache_milest_stats(milestone_id)
    data = cache.get(f'milestone:{milestone_id}')
  else:
    print(f'the milestone {milestone_id}')
    
  return data