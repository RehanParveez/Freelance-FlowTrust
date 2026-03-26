from django.shortcuts import render
from rest_framework import viewsets
from notifications.serializers import NotificationSerializer
from notifications.models import Notification
from core.permissions import NotificationPermission

# Create your views here.
class NotificationViewset(viewsets.ModelViewSet):
  serializer_class = NotificationSerializer
  queryset = Notification.objects.all().order_by('id')
  permission_classes = [NotificationPermission]
