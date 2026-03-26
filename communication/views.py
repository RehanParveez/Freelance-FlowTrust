from django.shortcuts import render
from rest_framework import viewsets
from communication.serializers.detail import TalkSerializer, MessageSerializer, NegotiationSerializer
from communication.models import Talk, Message, Negotiation
from core.permissions import TalkPermission, MessagePermission, NegotiationPermission

# Create your views here.
class TalkViewset(viewsets.ModelViewSet):
  serializer_class = TalkSerializer
  queryset = Talk.objects.all().order_by('id')
  permission_classes = [TalkPermission]

class MessageViewset(viewsets.ModelViewSet):
  serializer_class = MessageSerializer
  queryset = Message.objects.all().order_by('id')
  permission_classes = [MessagePermission]
    
class NegotiationViewset(viewsets.ModelViewSet):
  serializer_class = NegotiationSerializer
  queryset = Negotiation.objects.all().order_by('id')
  permission_classes = [NegotiationPermission]
    


