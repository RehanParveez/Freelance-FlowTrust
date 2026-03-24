from rest_framework import serializers
from payments.serializers.basic import TransactionSerializer1, EscrowSerializer1, RefundSerializer1
from accounts.serializers.basic import UserSerializer1
from milestones.serializers.basic import MilestoneSerializer1
from payments.models import Wallet, Transaction, Escrow, Payment, Refund, PaymentMethod

class WalletSerializer(serializers.ModelSerializer):
  transactions = TransactionSerializer1(many=True, read_only=True)
  class Meta:
    model = Wallet
    fields = ['user', 'transactions', 'balance']
    
class TransactionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Transaction
    fields = ['wallet', 'amount', 'transaction', 'date', 'description']
    
class EscrowSerializer(serializers.ModelSerializer):
  milestone = MilestoneSerializer1(read_only=True)
  client = UserSerializer1(read_only=True)
  freelancer = UserSerializer1(read_only=True)
  class Meta:
    model = Escrow
    fields = ['milestone', 'client', 'freelancer', 'amount', 'is_funded', 'is_released', 'created_at']
    
class PaymentSerializer(serializers.ModelSerializer):
  escrow = EscrowSerializer1(read_only=True)
  client = UserSerializer1(read_only=True)
  freelancer = UserSerializer1(read_only=True)
  refunds = RefundSerializer1(many=True, read_only=True)
  class Meta:
    model = Payment
    fields = ['escrow', 'client', 'freelancer', 'refunds', 'amount', 'created_at']
    
class RefundSerializer(serializers.ModelSerializer):
  class Meta:
    model = Refund
    fields = ['payment', 'amount', 'reason', 'refunded_at']
    
class PaymentMethodSerializer(serializers.ModelSerializer):
  class Meta:
    model = PaymentMethod
    fields = ['user', 'method_type', 'is_default']