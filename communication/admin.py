from django.contrib import admin
from communication.models import Talk, Message, Negotiation 

# Register your models here.
@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
  list_display = ['contract', 'started_at', 'last_activity']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
  list_display = ['talk', 'by', 'content', 'read', 'sent_at'] 

@admin.register(Negotiation)
class NegotiationAdmin(admin.ModelAdmin):
  list_display = ['contract', 'initiator', 'status', 'created_at', 'updated_at']
  