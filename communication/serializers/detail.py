from rest_framework import serializers
from communication.serializers.basic import MessageSerializer1
from accounts.serializers.basic import UserSerializer1
from communication.models import Talk, Message, Negotiation

class TalkSerializer(serializers.ModelSerializer):
  messages = MessageSerializer1(many=True, read_only=True)
  class Meta:
    model = Talk
    fields = ['contract', 'messages', 'participants', 'started_at', 'last_activity']
      
class MessageSerializer(serializers.ModelSerializer):
  by = UserSerializer1(read_only=True)
  class Meta:
    model = Message
    fields = ['talk', 'by', 'content', 'read', 'sent_at']

class NegotiationSerializer(serializers.ModelSerializer):
  initiator = UserSerializer1(read_only=True)
  class Meta:
    model = Negotiation
    fields = ['contract', 'initiator', 'status', 'created_at', 'updated_at']