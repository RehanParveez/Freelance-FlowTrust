from django.contrib import admin
from contracts.models import Contract, ContrParticipant, ContractTerm, ContractStatus, Activity

# Register your models here.
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
  list_display = ['client', 'freelancer', 'title', 'description', 'total_amount', 'status', 'created_at']

@admin.register(ContrParticipant)
class ContractParticipantAdmin(admin.ModelAdmin):
  list_display = ['contract', 'user', 'role']    

@admin.register(ContractTerm)
class ContractTermAdmin(admin.ModelAdmin):
  list_display = ['contract', 'description', 'created_at']
  
@admin.register(ContractStatus)
class ContractStatusAdmin(admin.ModelAdmin):
  list_display = ['contract', 'prev_status', 'new_status', 'changed_by', 'date']
  
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
  list_display = ['user', 'action_type', 'content_type', 'object_id', 'content_object', 'date']