from rest_framework import serializers
from payments.models import Transaction, Escrow, Payment, Refund
 
class TransactionSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Transaction
    fields = ['wallet', 'amount', 'transaction']
    
class EscrowSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Escrow
    fields = ['milestone', 'client', 'freelancer', 'amount']
    
class PaymentSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Payment
    fields = ['escrow', 'client', 'freelancer']
    
class RefundSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Refund
    fields = ['payment', 'amount']
    
