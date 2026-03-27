from rest_framework import viewsets
from communication.serializers.detail import TalkSerializer, MessageSerializer, NegotiationSerializer
from communication.models import Talk, Message, Negotiation
from core.permissions import ParticipantOrAdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class TalkViewset(viewsets.ModelViewSet):
  serializer_class = TalkSerializer
  queryset = Talk.objects.all().order_by('id')
  permission_classes = [ParticipantOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['last_activity']
  ordering_fields = ['started_at']
  filterset_fields = ['last_activity', 'started_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    return self.queryset.filter(participants=user)

class MessageViewset(viewsets.ModelViewSet):
  serializer_class = MessageSerializer
  queryset = Message.objects.all().order_by('id')
  permission_classes = [ParticipantOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['content']
  ordering_fields = ['sent_at']
  filterset_fields = ['content', 'sent_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    return self.queryset.filter(talk__participants=user)
    
class NegotiationViewset(viewsets.ModelViewSet):
  serializer_class = NegotiationSerializer
  queryset = Negotiation.objects.all().order_by('id')
  permission_classes = [ParticipantOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['status']
  ordering_fields = ['created_at']
  filterset_fields = ['status', 'created_at', 'updated_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    client_nego = self.queryset.filter(contract__client=user)
    freel_nego = self.queryset.filter(contract__freelancer=user)
    return client_nego | freel_nego
  
  
    


