from django.shortcuts import render
from rest_framework import viewsets
from notifications.serializers import NotificationSerializer
from notifications.models import Notification
from core.permissions import NotificationPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class NotificationViewset(viewsets.ModelViewSet):
  serializer_class = NotificationSerializer
  queryset = Notification.objects.all().order_by('id')
  permission_classes = [NotificationPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['event_type']
  ordering_fields = ['created_at']
  filterset_fields = ['content', 'read', 'created_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    return self.queryset.filter(user=user)
