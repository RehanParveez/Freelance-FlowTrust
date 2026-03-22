from django.contrib import admin
from payments.models import Wallet, Escrow, Payment

# Register your models here.
@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
    
@admin.register(Escrow)
class EscrowAdmin(admin.ModelAdmin):
    list_display = ['milestone', 'client', 'freelancer', 'amount', 'is_funded', 'is_released', 'created_at']
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['escrow', 'client', 'freelancer', 'amount', 'created_at']

