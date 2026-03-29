from payments.models import Wallet
from django.core.cache import cache
from decimal import Decimal

def cache_wallet(user_id):
  wallet = Wallet.objects.get(user_id=user_id)
  cache.set(f'wallet:{user_id}', str(wallet.balance))
  print(f'the upd wallet for the user {user_id}: {wallet.balance}')

def get_wallet_bal(user_id):
  bal = cache.get(f'wallet:{user_id}')
  if bal is None:
    wallet_bal = Wallet.objects.get(user_id=user_id).balance
    
    cache.set(f'wallet:{user_id}', str(wallet_bal))
    print(f'the cached wallet for the user {user_id}: {wallet_bal}')
    return wallet_bal
  print(f'generated wallet for the user {user_id}: {bal}')
  
  return Decimal(bal)