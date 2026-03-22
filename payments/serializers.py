from rest_framework import serializers
from payments.models import Wallet, Escrow, Payment

class WalletSerializer(serializers.ModelSerializer):
  class Meta:
    model = Wallet
    fields = ['user', 'balance']
    
class EscrowSerializer(serializers.ModelSerializer):
  class Meta:
    model = Escrow
    fields = ['milestone', 'client', 'freelancer', 'amount', 'is_funded', 'is_released', 'created_at']
    
class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Payment
    fields = ['escrow', 'client', 'freelancer', 'amount', 'created_at']