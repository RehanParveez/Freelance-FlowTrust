from django.contrib import admin
from disputes.models import Dispute, DisputeMessage, Proof, Solution

# Register your models here.
@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
  list_display = ['contract', 'milestone', 'raised_by', 'description', 'status', 'created_at', 'updated_at']

@admin.register(DisputeMessage)
class DisputeMessageAdmin(admin.ModelAdmin):
  list_display = ['dispute', 'by', 'content', 'created_at']    

@admin.register(Proof)
class ProofAdmin(admin.ModelAdmin):
  list_display = ['dispute', 'file', 'description', 'uploaded_at']
  
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
  list_display = ['dispute', 'decision', 'solved_by', 'solved_at', 'amount_rel_to_freel', 'amount_ref_to_client']
