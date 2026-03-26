from rest_framework import serializers
from notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notification
    fields = ['user', 'content', 'event_type', 'read', 'created_at']