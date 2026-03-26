from rest_framework import serializers
from communication.models import Message, Negotiation

class MessageSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = ['talk', 'by', 'content']
    
class NegotiationSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Negotiation
    fields = ['contract', 'initiator']