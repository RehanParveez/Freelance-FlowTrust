from django.contrib import admin
from milestones.models import Milestone

# Register your models here.
@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
  list_display = ['contract', 'title', 'amount', 'status', 'is_submitted', 'is_approved']
    