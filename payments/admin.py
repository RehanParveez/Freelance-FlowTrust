from django.contrib import admin
from payments.models import Wallet, Transaction, Escrow, Payment, Refund, PaymentMethod

# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'amount', 'transaction', 'date', 'description']   
     
@admin.register(Escrow)
class EscrowAdmin(admin.ModelAdmin):
    list_display = ['milestone', 'client', 'freelancer', 'amount', 'is_funded', 'is_released', 'created_at']
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['escrow', 'client', 'freelancer', 'amount', 'created_at']
    
@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['payment', 'amount', 'reason', 'refunded_at']
    
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'method_type', 'is_default']

