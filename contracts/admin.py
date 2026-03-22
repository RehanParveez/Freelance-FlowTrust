from django.contrib import admin
from contracts.models import Contract

# Register your models here.
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
  list_display = ['client', 'freelancer', 'title', 'description', 'total_amount', 'status', 'created_at']
    
